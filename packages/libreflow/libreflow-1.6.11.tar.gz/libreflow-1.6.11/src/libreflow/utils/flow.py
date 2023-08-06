import sys
import zipfile
import sys
import os
import shutil
from string import Formatter
from collections import OrderedDict

from kabaret.flow_contextual_dict import get_contextual_dict


def _keywords_from_format(format):
    return [fname for _, fname, _, _ in Formatter().parse(format) if fname]


def _get_param_values(leaf, name, level=0, max_level=sys.maxsize):
    session = leaf.root().session()
    param_oid = leaf.oid() + '/' + name
    values = []
    
    if session.cmds.Flow.exists(param_oid):
        value = session.cmds.Flow.get_value(param_oid)
        values.append(value)
    
    parent = leaf._mng.parent
    
    if parent is not leaf.root() and level < max_level:
        parent_values = _get_param_values(parent, name, level + 1, max_level)
        return parent_values + values
    else:
        return values


def get_context_value(
        leaf,
        param_name,
        delim='',
        context_name='settings',
        max_level=sys.maxsize,
    ):
    
    session = leaf.root().session()
    
    # Recursively search param
    param_values = _get_param_values(leaf, param_name, max_level=max_level)
    
    if not param_values:
        return None
    
    # Build context value from accumulated values
    context_value = delim.join(param_values)
    
    # Search for contextual keys
    try:
        keys = _keywords_from_format(context_value)
    except ValueError:
        session.log_error((
            f"Invalid value format \"{context_value}\"\n\n"
            "<<<<<<<<<<< TRACEBACK >>>>>>>>>>\n"
        ))
        raise
    
    if keys:
        # Get contextual values
        context = get_contextual_dict(leaf, context_name)
        values = OrderedDict()
        
        for key in keys:
            try:
                values[key] = context[key]
            except KeyError:
                session.log_error((
                    f"No key \"{key}\" in {leaf.oid()} context\n\n"
                    "<<<<<<<<<<< TRACEBACK >>>>>>>>>>\n"
                ))
                raise
        
        context_value = context_value.format(**values)
    
    return context_value


def remove_folder_content(folder_path):
    '''
    Deletes the content of a folder located at `folder_path`
    without deleting the folder itself.
    
    From https://stackoverflow.com/a/185941
    '''
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            else:
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {folder_path} folder content.\n>>>\n{str(e)}')
            return False
    
    return True


def zip_folder(folder_path, output_path):
    '''
    Creates a ZIP archive with the content of the folder, located
    at `folder_path`, at its root (i.e., it skips the folder level
    itself in the resulting archive tree).
    '''
    # Initialise empty file paths list
    file_paths = []

    # Crawl through directory and subdirectories
    for root, directories, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # Writing files to a zipfile
    with zipfile.ZipFile(output_path,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file, arcname=file.replace(folder_path, ''))
