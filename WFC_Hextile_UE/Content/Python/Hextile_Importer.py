import unreal, sys, json

def gen_mapBP(_jsonFile, _bpLocation, _bpName):
    #print(_jsonFile, _bpLocation, _bpName)
    # Opening JSON file
    try:
        with open(_jsonFile) as json_file:
            jsonData = json.load(json_file)
    except Exception as err:
        print("Failed on reading the JSON file.{}".format(err))
        return
    #
    EASubsystem = unreal.EditorActorSubsystem()
    actor = EASubsystem.spawn_actor_from_class(unreal.Actor, unreal.Vector(0.0, 0.0, 0.0))
    actor.set_actor_label("HextileMap")
    # create bp
    # get the root data handle
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    root_data_handle = subsystem.k2_gather_subobject_data_for_instance(actor)[0]
    # iterate over the tiles
    for tile in jsonData.keys():
        # add sub object
        sub_handle, fail_reason = subsystem.add_new_subobject(
            unreal.AddNewSubobjectParams(
                parent_handle=root_data_handle,
                new_class=unreal.InstancedStaticMeshComponent
            ))
        if not fail_reason.is_empty():
            raise Exception("ERROR from sub_object_subsystem.add_new_subobject: {fail_reason}" )
        #
        subsystem.attach_subobject( root_data_handle, sub_handle )
        subsystem.rename_subobject(sub_handle, tile)
    #
    allCmps = actor.get_components_by_class(unreal.InstancedStaticMeshComponent)
    for comp in allCmps:
        smObject = unreal.load_asset(jsonData[comp.get_name()]["UEPath"])
        comp.set_editor_property("static_mesh", smObject)
        for idx, pos in enumerate(jsonData[comp.get_name()]["Pos"]):
            uPos = unreal.Vector(pos[0], pos[2], pos[1])
            rotVal = jsonData[comp.get_name()]["Rot"][idx]
            rot = unreal.Rotator(0.0, 0.0, rotVal*-60.0)
            transform = unreal.Transform(uPos, rot)
            comp.add_instance(transform)
            #print(idx, pos, jsonData[comp.get_name()]["Rot"][idx])


#
'''
D:\_MY\myProjects\ProceduralCity\WFC\kenney_hexagon-kit\Models\BGEO\JSON_ALL\HextileMap.json
/Game/Hextile_Map
HextileMap
'''