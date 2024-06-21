

const mesh = {
    indices: new Uint32Array(indices),
    vertices: new Float32Array(vertices),
    normals: new Float32Array(normals)
};

const encoderModule = DracoEncoderModule();
const encoder = new encoderModule.Encoder();
const meshBuilder = new encoderModule.MeshBuilder();
const dracoMesh = new encoderModule.Mesh();

const numFaces = mesh.indices.length / 3;
const numPoints = mesh.vertices.length;
meshBuilder.AddFacesToMesh(dracoMesh, numFaces, mesh.indices);

meshBuilder.AddFloatAttributeToMesh(dracoMesh, encoderModule.POSITION,
    numPoints, 3, mesh.vertices);
if (mesh.hasOwnProperty('normals')) {
    meshBuilder.AddFloatAttributeToMesh(
        dracoMesh, encoderModule.NORMAL, numPoints, 3, mesh.normals);
}
if (mesh.hasOwnProperty('colors')) {
    meshBuilder.AddFloatAttributeToMesh(
        dracoMesh, encoderModule.COLOR, numPoints, 3, mesh.colors);
}
if (mesh.hasOwnProperty('texcoords')) {
    meshBuilder.AddFloatAttributeToMesh(
        dracoMesh, encoderModule.TEX_COORD, numPoints, 3, mesh.texcoords);
}

if (method === "edgebreaker") {
    encoder.SetEncodingMethod(encoderModule.MESH_EDGEBREAKER_ENCODING);
} else if (method === "sequential") {
    encoder.SetEncodingMethod(encoderModule.MESH_SEQUENTIAL_ENCODING);
}

const encodedData = new encoderModule.DracoInt8Array();
// Use default encoding setting.
const encodedLen = encoder.EncodeMeshToDracoBuffer(dracoMesh,
    encodedData);
encoderModule.destroy(dracoMesh);
encoderModule.destroy(encoder);
encoderModule.destroy(meshBuilder);
