import os
import sys
import re
import logging
import tempfile
from pytz import timezone

from ds_plugin.common import io_utils
from ds_plugin.pusher import ceto_publisher, cyclone_publisher
from ds_plugin.common.utils import hdfs_utils

SG_HDFS = "bigocluster"
EU_HDFS = "bigo-eu"
CETO_MODEL_BASE_DIR = f"hdfs://{SG_HDFS}/data/models"
CETO_EMB_BASE_DIR = f"hdfs://{SG_HDFS}/data/embs"

def handle_path(self, path_in, dim):
    idx = [f.start() for f in re.finditer("/", path_in)]
    assert len(idx) > 2
    assert path_in.split("/")[-3] == dim
    path_out = path_in[: (idx[-3] + 1)]
    return path_out

def parse_shard_info(self, emb_bin_path, model_version, is_eu):
    shards = {}

    fs, path = io_utils.resolve_filesystem_and_path(emb_bin_path)
    path_set = set()
    for fpath in fs.ls(path):
        if fpath.find("emb_bin/meta_") < 0:
            raise ValueError(
                "Invalid emb bin meta file %s, should contains 'emb_bin/meta_'"
                % fpath
            )
        part = int(fpath.split("emb_bin/meta_")[1])
        file_content = io_utils.read_file_string(fpath).decode()
        for line in file_content.split("\n"):
            if not line or len(line) <= 8:
                continue
            dim, misc = line[8:].split("|", 1)

            shards.setdefault(dim, [])

            path, start, end, count, size = misc.split(",", 4)
            sg_emb_path = os.path.join(CETO_EMB_BASE_DIR, path)

            path_cp = self.handle_path(sg_emb_path, dim)
            logging.info(f"sg_emb_path: {sg_emb_path}, path_cp: {path_cp}")
            path_set.add(path_cp)

            shard = {
                "shard_idx": part,
                "tail_number_start": int(start),
                "tail_number_end": int(end),
                "sub_models": [
                    {
                        "model_uri": sg_emb_path,
                        "publish_time": model_version,
                        "hdfs_path": sg_emb_path,
                        "sub_version": str(model_version),
                        "keys_count": int(count),
                        "data_size": int(size),
                    }
                ],
            }

            shards[dim].append(shard)
    if is_eu:
        # 如果发布到欧洲需要同步emb
        # path_set集合应该只含一个值，是以version结尾的emb路径
        logging.info("path_set: {}".format(path_set))
        assert len(path_set) == 1
        for pth in path_set:
            ret = hdfs_utils.sync_to_eu_local_hdfs(pth, SG_HDFS)
            if ret:
                logging.info(
                    "[Success] sync {} to eu local_hdfs.".format(pth)
                )
            else:
                raise RuntimeError(
                    "[Failed] sync {} to eu local_hdfs!".format(pth)
                )

    return shards

def publish_embeddings(
    self,
    model_name,
    model_version,
    emb_bin_path,
    target,
    timeout_s,
):
    is_sg = True if "sg" in target else False
    is_eu = True if "eu" in target else False
    all_shards = self._parse_shard_info(emb_bin_path, model_version, is_eu)
    logging.info(
        "begin to publish model embedding to cyclone, embedding dims are %s",
        ",".join([dim for dim in all_shards]),
    )

    for dim, shards in all_shards.items():
        cyclone_model_name = f"{model_name}_{dim}"
        cyclone_options = cyclone_publisher.CycloneOptions(
            model_name=cyclone_model_name,
            model_version=model_version,  # 构造model name = name_dim
        )

        if not cyclone_publisher.publish_model_to_cyclone(
            cyclone_options, shards, is_eu, is_sg
        ):
            raise RuntimeError(
                "Failed to publish model to cyclone, dim: %d",
            )

    for dim, shards in all_shards.items():
        cyclone_model_name = f"{model_name}_{dim}"
        ret = cyclone_publisher.poll_cyclone_model_info(
            model_name=cyclone_model_name,
            model_version=model_version,
            timeout_s=timeout_s,
            is_eu=is_eu,
            is_sg=is_sg,
        )
        if not ret:
            raise RuntimeError("Failed to publish embedding")
        logging.info(
            "publish model embedding with dim(%s) to cyclone server successfully!",
            dim,
        )

def publish_graph(
    self, model_name, model_version, namespace, graph_path, target
):
    # copy file to ceto"s model dir
    graph_dir_name = os.path.basename(graph_path)
    ceto_model_path = (
        f"{CETO_MODEL_BASE_DIR}/{namespace}/{model_name}/{model_version}"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        io_utils.download_dir(
            graph_path, os.path.join(tmpdir, graph_dir_name)
        )
        if "sg" in target:
            io_utils.upload_dir(
                os.path.join(tmpdir, graph_dir_name), ceto_model_path
            )
        if "eu" in target:
            io_utils.upload_dir(
                os.path.join(tmpdir, graph_dir_name),
                ceto_model_path.replace(SG_HDFS, EU_HDFS),
            )
    # update meta to ceto
    meta_ceto_model_path = ("/%s" % "/".join(ceto_model_path.split("/")[3:]))
    for dest in target:
        ret = ceto_publisher.publish_model_to_ceto(
            model_name, namespace, model_version, meta_ceto_model_path, dest
        )
        if not ret:
            logging.error(
                "Failed to publish model to ceto, model name: %s, namespace: %s, model_version: %s, meta_ceto_model_path: %s",
                model_name,
                namespace,
                model_version,
                meta_ceto_model_path,
            )
            raise RuntimeError("Failed to publish model to ceto!")
    logging.info(
        "Successfully publish model to ceto, model name: %s, namespace: %s, model_version: %s, meta_ceto_model_path: %s",
        model_name,
        namespace,
        model_version,
        meta_ceto_model_path,
    )