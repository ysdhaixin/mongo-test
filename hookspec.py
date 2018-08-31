import os
import fnmatch
import pluggy


FILTERS = ()

spec = pluggy.HookspecMarker("data-mgr")
impl = pluggy.HookimplMarker("data-mgr")


class DataSourceSpec:
    @spec
    def load_source(self, path):
        """load data source by its path, for example, file system like path, net access,
         or a raw text
        """

    @spec
    def retrieve_document(self, item, *attr, **kargv):
        """by type checking to get the document
        """


class Plugin:
    @impl
    def load_source(self, path):
        assert path
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        def _get_all_files(path):
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if fnmatch.fnmatch(file, '*.mp4'):
                            yield os.path.join(root, file)
            else:
                yield path

        # to parse excel
        def _get_item_excel(path):
            return path

        item_paths = _get_all_files(path)
        for item in item_paths:
            if fnmatch.fnmatch(item, '*.xls'):
                yield _get_item_excel(item)
            else:
                yield item

    @impl
    def wrap_document(self, item, *attr, **kargv):
        def check_item_size(item):
            return True

        if check_item_size(item):
            pass




