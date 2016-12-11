
// Assembiles are for grouping faces and other assembiles
function createAssembly() {
    var assembly = document.createElement("div");
    assembly.className = "threedee assembly";
    return assembly;
}

function createFace(w, h, x, y, z, rx, ry, rz, bgcolor, tx, ty, did = "", extraclasses="") {
    var face = document.createElement("div");
    face.id = did;
    face.className = "threedee face material-animation " + extraclasses;
    face.style.cssText = PrefixFree.prefixCSS(
        "background-color: " + bgcolor + ";" +
        "background-size: " + tx + " " + ty + ";" +
        "width:" + w + ";" +
        "height:" + h + ";" +
        "transform: translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px," + z.toFixed(2) + "px)" +
        "rotateX(" + rx.toFixed(2) + "rad) rotateY(" + ry.toFixed(2) + "rad) rotateY(" + rz.toFixed(2) + "rad);");
    return face;
}

function createTube(dia, height, sides, texture) {
    var tube = createAssembly();
    var sideAngle = (Math.PI / sides) * 2;
    var sideLen = dia * Math.tan(Math.PI/sides);
    for (var c = 0; c < sides; c++) {
        var x = Math.sin(sideAngle * c) * dia / 2;
        var z = Math.cos(sideAngle * c) * dia / 2;
        var ry = Math.atan2(x, z);
        tube.appendChild(createFace(sideLen + 1, height, x, 0, z, 0, ry, 0, texture, sideLen * c, 0));
    }
    return tube;
}

function createBarrel(texture) {
    var barrel = createTube(100, 196, 20, texture);
    barrel.appendChild(createFace(100, 100, 0, -98, 0, Math.PI / 2, 0, 0, texture, 0, 100));
    barrel.appendChild(createFace(100, 100, 0, 98, 0, -Math.PI / 2, 0, 0, texture, 0, 100));
    return barrel;
}

function updateFaces() {
    $('.material-animation').each(function() {
        if($(this).hasClass('circle')) {
            var thisid = this.id;
            var face = document.getElementById(thisid);
            $(face).css("height", face.offsetWidth.toFixed(2) + "px");
        }
    });
}

function getTransform(el) {
    var results = $(el).css('-webkit-transform').match(/matrix(?:(3d)\(\d+(?:, \d+)*(?:, (\d+))(?:, (\d+))(?:, (\d+)), \d+\)|\(\d+(?:, \d+)*(?:, (\d+))(?:, (\d+))\))/)

    if(!results) return [0, 0, 0];
    if(results[1] == '3d') return results.slice(2,5);

    results.push(0);
    return results.slice(5, 8);
}

function createShadowDiv(PointLightSourceInstance, shadowLevel, MaterialDivInstance, sid="") {
    var div = MaterialDivInstance.div;
    var transformCoordinates = getTransform(div);
    var offsetZ = transformCoordinates[2];
    var offsetX = getOffsetRect(div).left;
    var offsetY = getOffsetRect(div).top;
    var height = $(div).outerHeight();
    var width = $(div).outerWidth();
    var shadowDict = MaterialDivInstance.calculatePointShadow(PointLightSourceInstance, shadowLevel, offsetX, offsetY, offsetZ, height, width);
    var shadowIntensity = shadowDict.shadowIntensity;
    var shadowRelativeOffset = MaterialDivInstance.calculatePointShadowOffset(PointLightSourceInstance, shadowLevel, offsetX, offsetY, offsetZ);
    var shadowRelativeOffsetX = shadowRelativeOffset.relativeOffsetX;
    var shadowRelativeOffsetY = shadowRelativeOffset.relativeOffsetY;
    var z = - parseInt(offsetZ) + shadowLevel + 1;
    var maxX = shadowDict.offsetMaxX;
    var maxY = shadowDict.offsetMaxY;
    var minX = shadowDict.offsetMinX;
    var minY = shadowDict.offsetMinY;
    var w = Math.abs(maxX - minX);
    var h = Math.abs(maxY - minY);
    var opacity = (shadowIntensity/CombinedLightIntensity);

    var shadow = document.createElement("div");
    shadow.className = "threedee face shadow ";
    shadow.id = sid;
    shadow.style.cssText = PrefixFree.prefixCSS(
        "background-color: rgba(0,0,0," + opacity.toFixed(2) + ");" +
        "background-size: " + w.toFixed(2) + "px " + h.toFixed(2) + "px;" +
        "width:" + w.toFixed(2) + "px;" +
        "height:" + h.toFixed(2) + "px;" +
        "transform: translate3d(" + shadowRelativeOffsetX.toFixed(2) + "px," + shadowRelativeOffsetY.toFixed(2) + "px," + z.toFixed(2) + "px)"
        );
    div.appendChild(shadow);
}

function constructShadows() {
    var totalDivs = MaterialDivsAllInstances.length;
    var totalLights = PointLightSourcesAllInstances.length;
    var totalShadowLevels = HighestZ - 1;
    var z;
    var index1;
    var index2;
    var sid;
    $('.shadow').remove();

    for(z=1; z<HighestZ; z+10) {
        for(index1=0; index1 < totalDivs;) {
            for(index2=0; index2 < totalLights;) {
                sid = "shadow-" + index1.toFixed(2) + "-" + index2.toFixed(2);
                createShadowDiv(PointLightSourcesAllInstances[index2],z, MaterialDivsAllInstances[index1], sid);
                index2 = index2 + 1;
            }
            index1 = index1 + 1;
        }
        z = z+10;
    }
}

function getOffsetRect(elem) {
    // (1)
    var box = elem.getBoundingClientRect()

    var body = document.body
    var docElem = document.documentElement

    // (2)
    var scrollTop = window.pageYOffset || docElem.scrollTop || body.scrollTop
    var scrollLeft = window.pageXOffset || docElem.scrollLeft || body.scrollLeft

    // (3)
    var clientTop = docElem.clientTop || body.clientTop || 0
    var clientLeft = docElem.clientLeft || body.clientLeft || 0

    // (4)
    var top  = box.top +  scrollTop - clientTop
    var left = box.left + scrollLeft - clientLeft

    return { top: Math.round(top), left: Math.round(left) }
}
