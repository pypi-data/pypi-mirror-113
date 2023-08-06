import bpy


def tag_redraw():
    '''Redraw all regions.'''
    if hasattr(bpy.context, 'window_manager'):
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                for region in area.regions:
                    region.tag_redraw()
