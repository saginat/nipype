from nipype.pipeline.plugins.base import SGELikeBatchManagerBase
from nipype.interfaces.utility import Function
import nipype.pipeline.engine as pe
from os.path import join
import os
from glob import glob
import pytest
from unittest.mock import patch
from tempfile import TemporaryDirectory
import subprocess


def crasher():
    raise ValueError()

    
def submit_batchtask(self, scriptfile, node):    
    self._pending[1] = node.output_dir()
    subprocess.call(["bash", scriptfile])
    return 1


def is_pending(self, taskid):
    return False


@patch.object(SGELikeBatchManagerBase, '_submit_batchtask', new=submit_batchtask)
@patch.object(SGELikeBatchManagerBase, '_is_pending', new=is_pending)
def test_crashfile_creation(tmp_path):
        pipe = pe.Workflow(name="pipe", base_dir=str(tmp_path))
        pipe.config["execution"]["crashdump_dir"] = str(tmp_path)
        pipe.add_nodes([pe.Node(interface=Function(function=crasher), 
                            name="crasher")])    
        sgelike_plugin = SGELikeBatchManagerBase("")
        with pytest.raises(RuntimeError) as e:
            assert pipe.run(plugin=sgelike_plugin)
        assert (str(e.value) == 
                "Workflow did not execute cleanly. Check log for details")
        
        crashfiles = tmp_path.glob("crash*crasher*.pklz")
        assert len(crashfiles) == 1
