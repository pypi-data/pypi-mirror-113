import os,sys
import logging
from ds_plugin.proto import artifact_pb2
from ds_plugin.common import io_utils

class Executor(object):
    def resolve_output_meta(self, meta_path: str, output_name: str):
        meta_pb = io_utils.parse_pbtxt_file(
            meta_path, artifact_pb2.Artifact(),
        )
        assert len(meta_pb.out) > 0
        for output in meta_pb.out:
            if output.name == output_name:
                return output.uri
        logging.warning("%s does not have output \{%s\}", meta_path, output_name)
        return None

    def save_out_meta(self, meta_uri_dict: dict, meta_path: str):
        assert type(meta_uri_dict) == dict
        assert len(meta_uri_dict) > 0

        meta_pb = artifact_pb2.Artifact()
        for name, uri in meta_uri_dict.items():
            output = meta_pb.out.add()
            output.name = name
            if type(meta_uri_dict[name]) == list:
                output.uri.extend(uri)
            elif type(meta_uri_dict[name]) == str:
                output.uri.append(uri)
            else:
                logging.warning(
                    "[OUT META] output of %s is None because %s is not list or string",
                    name, uri
                )
                
        io_utils.write_pbtxt_file(meta_path, meta_pb)
        logging.info("[OUT META] output meta information is here --> %s", meta_path)