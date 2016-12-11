var PointLightSourcesAllInstances = [];
var SphereLightSourcesAllInstances = [];
var MaterialDivsAllInstances = [];
var DivLayersAllInstances = [];
var CombinedLightIntensity = 0;
var PopulatedLevels = [];
var HighestZ = 0;

class DivLayer {
    constructor(z) {
        this.z = z;
        this.D = [];
        DivLayersAllInstances[(z/10)] = this;
    }

    update() {
        var sizeD = Math.size(this.D);
        if(sizeD[0] != Math.round($('body').width()*1.5) || sizeD[1] != Math.round($('body').height()*1.5)) {
            this.D = math.zeros(Math.round($('body').width()*1.5), Math.round($('body').height()*1.5));
        }
        var DivsAmount = MaterialDivsAllInstances.length;
        var index1;
        for(index1 = 0; index1 < DivsAmount; index1++) {
            if(MaterialDivsAllInstances[index1].z = this.z) {
                var div = MaterialDivsAllInstances[index1];
                var width = $(div).outerWidth();
                var height = $(div).outerHeight();
                var offsetX = getOffsetRect(div).left;
                var offsetY = getOffsetRect(div).top;
                var index2;
                for(index2=offsetX + Math.round($('body').width()*0.5); index2<=offsetX+width + Math.round($('body').width()*0.5); index2++) {
                    var index3;
                    for(index3=offsetY; index3<=offsetY+height; index3++) {
                        var size = math.size(this.D);
                        if(index2<=size[0] && index2>=0 && index3<=size[1] && index3>=0) {
                            this.D[index2,index3] = div.inDiv(index2-Math.round($('body').width()*0.5),index3-Math.round($('body').width()*0.5));
                        }
                    }
                }
            }
        }
    }
}

class ShadowLayer {
    constructor(z) {
        this.z = z;
        this.S = Math.zeros(1,1);
    }

    update() {
        var sizeS = Math.size(this.S);
        if(sizeS[0] != math.zeros($('body').width() || sizeS[1] != math.zeros($('body').height()) {
            this.S = math.zeros($('body').width(), $('body').height());
            sizeS = Math.size(this.S);
        }
        var index1;
        var index2;
        for(index1=0; index1<PointLightSourcesAllInstances.length; index1++) {
            for(index2=z+1; index2<=HighestZ; index2++) {
                var cdls = (index2 - PointLightSourcesAllInstances[index1].z)/(this.z - PointLightSourcesAllInstances[index1].z);
                var xs = range(0, sizeS[0]);
                var ys = range(0, sizeS[1]);
                xs = math.matrix(xs);
                ys = math.matrix(ys);
                var Xs = [];
                var Ys = [];
                (this.xs).map(function (value, index, matrix) {
                    Xs.push(Math.round((value - PointLightSourcesAllInstances[index1].x)*cdls));
                });
                (this.ys).map(function (value, index, matrix) {
                    Ys.push(Math.round((value - PointLightSourcesAllInstances[index1].y)*cdls));
                });

            }
        }
    }
}

class PointLightSource {
    constructor(x,y,z,intensity) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.intensity = intensity;
        PointLightSourcesAllInstances.push(this);
        CombinedLightIntensity += intensity;
    }

}

class SphereLightSource {
    constructor(x,y,z,radius,N=4,intensity) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.radius = radius;
        var index1;
        var index2;
        var pointLightArray = [];
        var alpha = (2*Math.PI) / N;
        /* construct x-constant circles */
        var dx = (2 * this.radius) / (N-1);
        for(index1=0; index1<=N-1; index1++) {
            var tempX = x - radius + index1 * dx;
            for(index2=1; index2<=N; index2++) {
                var tempY = ((tempX - x)^2 - (radius^2)) * Math.cos(index2 * alpha);
                var tempZ = ((tempX - x)^2 - (radius^2)) * Math.sin(index2 * alpha);
                var pointLight = new PointLightSource(tempX,tempY,tempZ,intensity);
                pointLightArray.push(pointLight);
            }
        }
        /* construct y-constant circles */
        var dy = (2 * this.radius) / (N-1);
        for(index1=0; index1<=N-1; index1++) {
            var tempY = y - radius + index1 * dy;
            for(index2=1; index2<=N; index2++) {
                var tempX = ((tempY - y)^2 - (radius^2)) * Math.cos(index2 * alpha);
                var tempZ = ((tempY - y)^2 - (radius^2)) * Math.sin(index2 * alpha);
                var pointLight = new PointLightSource(tempX,tempY,tempZ,intensity);
                pointLightArray.push(pointLight);
            }
        }
        /* construct z-constant circles */
        var dz = (2 * this.radius) / (N-1);
        for(index1=0; index1<=N-1; index1++) {
            var tempZ = z - radius + index1 * dz;
            for(index2=1; index2<=N; index2++) {
                var tempX = ((tempZ - z)^2 - (radius^2)) * Math.cos(index2 * alpha);
                var tempY = ((tempZ - z)^2 - (radius^2)) * Math.sin(index2 * alpha);
                var pointLight = new PointLightSource(tempX,tempY,tempZ,intensity);
                pointLightArray.push(pointLight);
            }
        }

        this.pointlights = pointLightArray;
        SphereLightSourcesAllInstances.push(this);
    }
}

class MaterialDiv {
    constructor(w, h, x, y, z, rx, ry, rz, bgcolor, tx, ty, did = "", extraclasses="", parent) {
        this.parent = parent;
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
        this.div = face;
        MaterialDivsAllInstances.push(this);
        var index = 0;
        if(jQuery.inArray(z,PopulatedLevels)<0) {
            for(index = HighestZ; index <= z;) {
                var dl = new DivLayer(index);
                PopulatedLevels.push(index);
                index = index + 10;
            }
        }
        HighestZ = Math.max(HighestZ, z);
    }

    inDiv(xCo,yCo,zCo) {
        var div = this.div;
        var width = $(div).outerWidth();
        var height = $(div).outerHeight();
        var offsetX = getOffsetRect(div).left;
        var offsetY = getOffsetRect(div).top;
        var centerX = offsetX + width/2;
        var centerY = offsetY + height/2;
        if($(this.div).hasClass("circle")) {
            var c = (xCo - centerX)^2 + (yCo - centerY)^2 - (width/2)^2;
            if(c<=0) {
                return 1;
            } else {
                return 0;
            }
        } else {
            if($(this.div).hasClass("ellipse")) {
                var c = ((xCo - centerX)/(width/2))^2 + ((yCo - centerY)/(height/2))^2 - 1;
                if(c<=0) {
                    return 1;
                } else {
                    return 0;
                }
            } else {
                var cx = (xCo - offsetX)*(offsetX + width - xCo);
                var cy = (yCo - offsetY)*(offsetY + height - yCo);
                if(cx>=0 && cy>=0) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }
    }

    calculatePointShadowOffset(PointLightSourceInstance, shadowLevel, offsetX, offsetY, offsetZ) {
        var xl = PointLightSourceInstance.x;
        var yl = PointLightSourceInstance.y;
        var zl = PointLightSourceInstance.z;
        var gammaZ = shadowLevel;
        var vx = offsetX - xl;
        var vy = offsetY - yl;
        var vz = offsetZ - zl;
        var relativeOffsetX = xl + (vx/vz) * (gammaZ - zl) - offsetX;
        var relativeOffsetY = yl + (vy/vz) * (gammaZ - zl) - offsetY;
        return {relativeOffsetX: relativeOffsetX, relativeOffsetY: relativeOffsetY};
    }

    calculatePointShadowPoint(PointLightSourceInstance, shadowLevel, offsetX, offsetY, offsetZ, xp, yp, height, width) {
        var shadow = 0;
        var xl = PointLightSourceInstance.x;
        var yl = PointLightSourceInstance.y;
        var zl = PointLightSourceInstance.z;
        var gammaZ = shadowLevel;
        var vx = xp - xl;
        var vy = yp - yl;
        var vxMin = offsetX - xl;
        var vyMin = offsetY - yl;
        var vxMax = offsetX + width - xl;
        var vyMax = offsetY + height - yl;
        var vz = offsetZ - zl;
        var offsetX = xl + (vx/vz) * (gammaZ - zl);
        var offsetY = yl + (vy/vz) * (gammaZ - zl);
        var offsetMinX = xl + (vxMin/vz) * (gammaZ - zl);
        var offsetMinY = yl + (vyMin/vz) * (gammaZ - zl);
        var offsetMaxX = xl + (vxMax/vz) * (gammaZ - zl);
        var offsetMaxY = yl + (vyMax/vz) * (gammaZ - zl);

        if($(this.div).hasClass('circle')) {
            var radius = width / 2;
            var c = offsetX^2 + offsetY^2 - radius^2;
            if(c<=0) {
                shadow = PointLightSourceInstance.intensity;
            }
        }

        if((!$(this.div).hasClass('circle')) && !$(this.div).hasClass('ellipse')) {
            if(((xp - offsetMinX)<=0) && ((xp - offsetMaxX)>=0) && ((yp - offsetMinY)<=0) && ((yp - offsetMaxY)>=0)) {
                shadow = PointLightSourceInstance.intensity;
            }
        }

        return shadow;
    }

    calculatePointShadow(PointLightSourceInstance, shadowLevel, offsetX, offsetY, offsetZ, height, width) {
        var xl = PointLightSourceInstance.x;
        var yl = PointLightSourceInstance.y;
        var zl = PointLightSourceInstance.z;
        var gammaZ = shadowLevel;
        var vxMin = offsetX - xl;
        var vyMin = offsetY - yl;
        var vxMax = offsetX + width - xl;
        var vyMax = offsetY + height - yl;
        var vz = offsetZ - zl;
        var offsetMinX = xl + (vxMin/vz) * (gammaZ - zl);
        var offsetMinY = yl + (vyMin/vz) * (gammaZ - zl);
        var offsetMaxX = xl + (vxMax/vz) * (gammaZ - zl);
        var offsetMaxY = yl + (vyMax/vz) * (gammaZ - zl);
        var shadow = PointLightSourceInstance.intensity;
        var relativeCenterX = offsetMinX + width/2 - offsetX;
        var relativeCenterY = offsetMinY + height/2 - offsetY;

        return {shadowIntensity: shadow, relativeCenterX: relativeCenterX, relativeCenterY: relativeCenterY, offsetMaxX: offsetMaxX, offsetMaxY: offsetMaxY, offsetMinX: offsetMinX, offsetMinY: offsetMinY};
    }
}
