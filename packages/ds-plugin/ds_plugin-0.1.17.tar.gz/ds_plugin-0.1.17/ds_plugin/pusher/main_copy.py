import os
import sys
import logging
import re
import functools
import time
import hashlib
import tempfile
import click
from datetime import datetime, timedelta
from pytz import timezone
from typing import Any, Dict, List, Text

from ds_plugin.executor import Executor
from ds_plugin.proto import schema_pb2, model_pb2, artifact_pb2
from ds_plugin.common import io_utils

from ds_plugin.pusher import ceto_publisher, cyclone_publisher
from ds_plugin.pusher import rtp_validator
from ds_plugin.pusher import local_emb_publish, remote_emb_publish
from ds_plugin.common.utils import hdfs_utils

SG_HDFS = "bigocluster"
EU_HDFS = "bigo-eu"
CETO_MODEL_BASE_DIR = f"hdfs://{SG_HDFS}/data/models"
CETO_EMB_BASE_DIR = f"hdfs://{SG_HDFS}/data/embs"


# class PusherExecutor(object):
#     def _resolve_converted_model_meta(self, model_meta_path):
#         model_pb = io_utils.parse_pbtxt_file(
#             os.path.join(model_meta_path, "converted_model.pbtxt"),
#             model_pb2.ConvertedModel(),
#         )

#         if not (model_pb and model_pb.embedding_path and model_pb.graph_path):
#             raise RuntimeError(
#                 "invalid model meta info parsed from %s" % model_meta_path
#             )
#         logging.info("parsed pushed model meta info: %s", model_pb)

#         fs, path = io_utils.resolve_filesystem_and_path(model_pb.embedding_path)
#         if not fs.exists(path):
#             raise RuntimeError(
#                 "model embedding path %s does not exist!"
#                 % model_pb.embedding_path
#             )

#         fs, path = io_utils.resolve_filesystem_and_path(model_pb.graph_path)
#         if not fs.exists(path):
#             raise RuntimeError(
#                 "model graph path %s does not exist!" % model_pb.graph_path
#             )

#         return model_pb

    # def handle_path(self, path_in, dim):
    #     idx = [f.start() for f in re.finditer("/", path_in)]
    #     assert len(idx) > 2
    #     assert path_in.split("/")[-3] == dim
    #     path_out = path_in[: (idx[-3] + 1)]
    #     return path_out

    # def _parse_shard_info(self, emb_bin_path, model_version, is_eu):
    #     shards = {}

    #     fs, path = io_utils.resolve_filesystem_and_path(emb_bin_path)
    #     path_set = set()
    #     for fpath in fs.ls(path):
    #         if fpath.find("emb_bin/meta_") < 0:
    #             raise ValueError(
    #                 "Invalid emb bin meta file %s, should contains 'emb_bin/meta_'"
    #                 % fpath
    #             )
    #         part = int(fpath.split("emb_bin/meta_")[1])
    #         file_content = io_utils.read_file_string(fpath).decode()
    #         for line in file_content.split("\n"):
    #             if not line or len(line) <= 8:
    #                 continue
    #             dim, misc = line[8:].split("|", 1)

    #             shards.setdefault(dim, [])

    #             path, start, end, count, size = misc.split(",", 4)
    #             sg_emb_path = os.path.join(CETO_EMB_BASE_DIR, path)

    #             path_cp = self.handle_path(sg_emb_path, dim)
    #             logging.info(f"sg_emb_path: {sg_emb_path}, path_cp: {path_cp}")
    #             path_set.add(path_cp)

    #             shard = {
    #                 "shard_idx": part,
    #                 "tail_number_start": int(start),
    #                 "tail_number_end": int(end),
    #                 "sub_models": [
    #                     {
    #                         "model_uri": sg_emb_path,
    #                         "publish_time": model_version,
    #                         "hdfs_path": sg_emb_path,
    #                         "sub_version": str(model_version),
    #                         "keys_count": int(count),
    #                         "data_size": int(size),
    #                     }
    #                 ],
    #             }

    #             shards[dim].append(shard)
    #     if is_eu:
    #         # 如果发布到欧洲需要同步emb
    #         # path_set集合应该只含一个值，是以version结尾的emb路径
    #         logging.info("path_set: {}".format(path_set))
    #         assert len(path_set) == 1
    #         for pth in path_set:
    #             ret = hdfs_utils.sync_to_eu_local_hdfs(pth, SG_HDFS)
    #             if ret:
    #                 logging.info(
    #                     "[Success] sync {} to eu local_hdfs.".format(pth)
    #                 )
    #             else:
    #                 raise RuntimeError(
    #                     "[Failed] sync {} to eu local_hdfs!".format(pth)
    #                 )

    #     return shards

    # def publish_embeddings(
    #     self,
    #     model_name,
    #     model_version,
    #     emb_bin_path,
    #     target,
    #     timeout_s,
    # ):
    #     is_sg = True if "sg" in target else False
    #     is_eu = True if "eu" in target else False
    #     all_shards = self._parse_shard_info(emb_bin_path, model_version, is_eu)
    #     logging.info(
    #         "begin to publish model embedding to cyclone, embedding dims are %s",
    #         ",".join([dim for dim in all_shards]),
    #     )

    #     for dim, shards in all_shards.items():
    #         cyclone_model_name = f"{model_name}_{dim}"
    #         cyclone_options = cyclone_publisher.CycloneOptions(
    #             model_name=cyclone_model_name,
    #             model_version=model_version,  # 构造model name = name_dim
    #         )

    #         if not cyclone_publisher.publish_model_to_cyclone(
    #             cyclone_options, shards, is_eu, is_sg
    #         ):
    #             raise RuntimeError(
    #                 "Failed to publish model to cyclone, dim: %d",
    #             )

    #     for dim, shards in all_shards.items():
    #         cyclone_model_name = f"{model_name}_{dim}"
    #         ret = cyclone_publisher.poll_cyclone_model_info(
    #             model_name=cyclone_model_name,
    #             model_version=model_version,
    #             timeout_s=timeout_s,
    #             is_eu=is_eu,
    #             is_sg=is_sg,
    #         )
    #         if not ret:
    #             raise RuntimeError("Failed to publish embedding")
    #         logging.info(
    #             "publish model embedding with dim(%s) to cyclone server successfully!",
    #             dim,
    #         )

    # def publish_graph(
    #     self, model_name, model_version, namespace, graph_path, target
    # ):
    #     # copy file to ceto"s model dir
    #     graph_dir_name = os.path.basename(graph_path)
    #     ceto_model_path = (
    #         f"{CETO_MODEL_BASE_DIR}/{namespace}/{model_name}/{model_version}"
    #     )
    #     with tempfile.TemporaryDirectory() as tmpdir:
    #         io_utils.download_dir(
    #             graph_path, os.path.join(tmpdir, graph_dir_name)
    #         )
    #         if "sg" in target:
    #             io_utils.upload_dir(
    #                 os.path.join(tmpdir, graph_dir_name), ceto_model_path
    #             )
    #         if "eu" in target:
    #             io_utils.upload_dir(
    #                 os.path.join(tmpdir, graph_dir_name),
    #                 ceto_model_path.replace(SG_HDFS, EU_HDFS),
    #             )
    #     # update meta to ceto
    #     meta_ceto_model_path = ("/%s" % "/".join(ceto_model_path.split("/")[3:]))
    #     for dest in target:
    #         ret = ceto_publisher.publish_model_to_ceto(
    #             model_name, namespace, model_version, meta_ceto_model_path, dest
    #         )
    #         if not ret:
    #             logging.error(
    #                 "Failed to publish model to ceto, model name: %s, namespace: %s, model_version: %s, meta_ceto_model_path: %s",
    #                 model_name,
    #                 namespace,
    #                 model_version,
    #                 meta_ceto_model_path,
    #             )
    #             raise RuntimeError("Failed to publish model to ceto!")
    #     logging.info(
    #         "Successfully publish model to ceto, model name: %s, namespace: %s, model_version: %s, meta_ceto_model_path: %s",
    #         model_name,
    #         namespace,
    #         model_version,
    #         meta_ceto_model_path,
    #     )

    # def save_meta(
    #     self, meta_output_path, model_name, model_version, origin_model_path
    # ):
    #     logging.info("push finished, model meta gen to %s" % meta_output_path)
    #     pushed_model = model_pb2.PushedModel()
    #     pushed_model.version = model_version
    #     pushed_model.name = model_name
    #     pushed_model.origin_model_path = origin_model_path
    #     pushed_model.pushed_time = int(time.time())
    #     io_utils.write_pbtxt_file(
    #         os.path.join(meta_output_path, "pushed_model.pbtxt"), pushed_model
    #     )

    # def execute(
    #     self,
    #     input_dict: Dict[Text, List[Artifact]],
    #     output_dict: Dict[Text, List[Artifact]],
    #     exec_properties: Dict[Text, Any],
    # ):
    #     self._log_startup(input_dict, output_dict, exec_properties)

    #     assert (
    #         "converted_model" in input_dict
    #         and len(input_dict["converted_model"]) == 1
    #     )
    #     converted_model_meta = self._resolve_converted_model_meta(
    #         input_dict["converted_model"][0].meta.uri
    #     )

    #     model_name = exec_properties["model_name"]
    #     namespace = exec_properties["namespace"]
    #     # 在xdl convert 中, 指定了model version, 并且将embedding数据转换成zmap格式，存放在了ceto指定的embedding目录下的 model_version子目录下
    #     # 这里的model version 和 converted_model 的 model version 保持一致
    #     model_version = converted_model_meta.converted_model_version
    #     target = exec_properties["target"]
    #     is_test = exec_properties["cyclone_test"]
    #     validate_accuracy = exec_properties["validate_accuracy"]
    #     validate_rate = exec_properties["validate_rate"]
    #     cyclone_wait_timeout = exec_properties["cyclone_wait_timeout"]

    #     local_emb = exec_properties["local_emb"]
    #     logging.info("local_emb is %s", local_emb)

    #     # TODO: 后续增加前端的控制开关之后，这里要改
    #     validation_samples_path = None
    #     if (
    #         "validation_samples" in input_dict
    #         and len(input_dict["validation_samples"]) == 1
    #     ):
    #         validation_samples_path = input_dict["validation_samples"][
    #             0
    #         ].meta.uri

    #     if local_emb:
    #         # 本地模型发布
    #         local_emb_publish.publish_graph_and_emb(
    #             model_name,
    #             model_version,
    #             namespace,
    #             converted_model_meta.graph_path,
    #             converted_model_meta.embedding_path,
    #             target,
    #             validation_samples_path,
    #             validate_accuracy,
    #             validate_rate,
    #         )
    #     else:
    #         # remote模型发布

    #         # publish embedding
    #         self.publish_embeddings(
    #             model_name,
    #             model_version,
    #             converted_model_meta.embedding_path,
    #             target,
    #             cyclone_wait_timeout,
    #         )

    #         if validation_samples_path is not None:
    #             # validate_ahead
    #             check_res = rtp_validator.validate_ahead(
    #                 validation_samples_path,
    #                 converted_model_meta.graph_path,
    #                 model_name,
    #                 model_version,
    #                 validate_accuracy,
    #                 validate_rate,
    #                 target[0],
    #             )
    #             if check_res:
    #                 logging.info(
    #                     "============================================================"
    #                 )
    #                 logging.info("[validation_ahead] Pass!")
    #             else:
    #                 logging.info(
    #                     "============================================================"
    #                 )
    #                 logging.info("[validation_ahead] Fail!")
    #                 raise RuntimeError("Validation failed, stop publishing!")

    #         self.publish_graph(
    #             model_name,
    #             model_version,
    #             namespace,
    #             converted_model_meta.graph_path,
    #             target,
    #         )

    #     self.save_meta(
    #         artifact_utils.get_single_uri(output_dict["output"]),
    #         model_name,
    #         model_version,
    #         os.path.dirname(converted_model_meta.graph_path),
    #     )

class Pusher(Executor):
    _parse_shard_info = remote_emb_publish.parse_shard_info
    _publish_embeddings = remote_emb_publish.publish_embeddings
    _publish_graph = remote_emb_publish.publish_graph

    def execute(
        self,
        converted_model: str,
        validate_samples: str,
        output: str,
        model_name,
        namespace,
        target,
        local_emb,
        validate_accuracy,
        validate_rate,
        cyclone_wait_timeout,
        out_meta: str
    ):
        logging.info("converted_model: %s", converted_model)
        logging.info("out_meta: %s", out_meta)
        assert converted_model != None and converted_model != ""
        if converted_model.endswith(io_utils.OUT_META):
            uri_list = self.resolve_output_meta(converted_model, "converted_model")
            if uri_list is None:
                raise RuntimeError("converted_model is None")
            converted_model = uri_list[0]
        converted_model_meta = self._resolve_converted_model_meta(converted_model)

        model_version = converted_model_meta.converted_model_version

        validation_samples_path = None
        if validate_samples is not None and validate_samples != "":
            if validate_samples.endswith(io_utils.OUT_META):
                uri_list = self.resolve_output_meta(
                    validate_samples, "validate_samples"
                )
                if uri_list is None:
                    raise RuntimeError("validate_samples is None")
                validation_samples_path = uri_list[0]
            else:
                validation_samples_path = validate_samples

        if local_emb:
            # 本地模型发布
            local_emb_publish.publish_graph_and_emb(
                model_name,
                model_version,
                namespace,
                converted_model_meta.graph_path,
                converted_model_meta.embedding_path,
                target,
                validation_samples_path,
                validate_accuracy,
                validate_rate,
            )
        else:
            # remote模型发布

            # publish embedding
            self._publish_embeddings(
                model_name,
                model_version,
                converted_model_meta.embedding_path,
                target,
                cyclone_wait_timeout,
            )

            if validation_samples_path is not None:
                # validate_ahead
                check_res = rtp_validator.validate_ahead(
                    validation_samples_path,
                    converted_model_meta.graph_path,
                    model_name,
                    model_version,
                    validate_accuracy,
                    validate_rate,
                    target[0],
                )
                if check_res:
                    logging.info(
                        "============================================================"
                    )
                    logging.info("[validation_ahead] Pass!")
                else:
                    logging.info(
                        "============================================================"
                    )
                    logging.info("[validation_ahead] Fail!")
                    raise RuntimeError("Validation failed, stop publishing!")

            self._publish_graph(
                model_name,
                model_version,
                namespace,
                converted_model_meta.graph_path,
                target,
            )

        output_dir = output
        if output is None:
            output_dir = '/'.join(out_meta.split('/')[:-1])
        meta_uri_dict = self.save_meta(
            output_dir,
            model_name,
            model_version,
            os.path.dirname(converted_model_meta.graph_path),
        )
        self.save_out_meta(meta_uri_dict, out_meta)

    def _resolve_converted_model_meta(self, model_meta_path):
        model_pb = io_utils.parse_pbtxt_file(
            os.path.join(model_meta_path, "converted_model.pbtxt"),
            model_pb2.ConvertedModel(),
        )

        if not (model_pb and model_pb.embedding_path and model_pb.graph_path):
            raise RuntimeError(
                "invalid model meta info parsed from %s" % model_meta_path
            )
        logging.info("parsed pushed model meta info: %s", model_pb)

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.embedding_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model embedding path %s does not exist!"
                % model_pb.embedding_path
            )

        fs, path = io_utils.resolve_filesystem_and_path(model_pb.graph_path)
        if not fs.exists(path):
            raise RuntimeError(
                "model graph path %s does not exist!" % model_pb.graph_path
            )

        return model_pb

    def save_meta(
        self, meta_output_path, model_name, model_version, origin_model_path
    ):
        logging.info("push finished, model meta gen to %s" % meta_output_path)
        pushed_model = model_pb2.PushedModel()
        pushed_model.version = model_version
        pushed_model.name = model_name
        pushed_model.origin_model_path = origin_model_path
        pushed_model.pushed_time = int(time.time())
        io_utils.write_pbtxt_file(
            os.path.join(meta_output_path, "pushed_model.pbtxt"), pushed_model
        )
        uri = os.path.join(meta_output_path, "pushed_model.pbtxt")
        meta_uri_dict = {"pushed_model": uri}
        return meta_uri_dict