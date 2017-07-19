
from cloudify import ctx
import os

if __name__ == '__main__':
    final_path = ctx.instance.runtime_properties['final_path']
    os.remove(final_path)
