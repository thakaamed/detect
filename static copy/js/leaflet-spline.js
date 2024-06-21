parcelRequire = function (e, r, t, n) {
    var i, o = "function" == typeof parcelRequire && parcelRequire, u = "function" == typeof require && require;

    function f(t, n) {
        if (!r[t]) {
            if (!e[t]) {
                var i = "function" == typeof parcelRequire && parcelRequire;
                if (!n && i) return i(t, !0);
                if (o) return o(t, !0);
                if (u && "string" == typeof t) return u(t);
                var c = new Error("Cannot find module '" + t + "'");
                throw c.code = "MODULE_NOT_FOUND", c
            }
            p.resolve = function (r) {
                return e[t][1][r] || r
            }, p.cache = {};
            var l = r[t] = new f.Module(t);
            e[t][0].call(l.exports, p, l, l.exports, this)
        }
        return r[t].exports;

        function p(e) {
            return f(p.resolve(e))
        }
    }

    f.isParcelRequire = !0, f.Module = function (e) {
        this.id = e, this.bundle = f, this.exports = {}
    }, f.modules = e, f.cache = r, f.parent = o, f.register = function (r, t) {
        e[r] = [function (e, r) {
            r.exports = t
        }, {}]
    };
    for (var c = 0; c < t.length; c++) try {
        f(t[c])
    } catch (e) {
        i || (i = e)
    }
    if (t.length) {
        var l = f(t[t.length - 1]);
        "object" == typeof exports && "undefined" != typeof module ? module.exports = l : "function" == typeof define && define.amd ? define(function () {
            return l
        }) : n && (this[n] = l)
    }
    if (parcelRequire = f, i) throw i;
    return f
}({
    "BWvR": [function (require, module, exports) {

    }, {
        "./images/layers.png": [["layers.350ec81b.png", "igUS"], "igUS"],
        "./images/layers-2x.png": [["layers-2x.d8c4f271.png", "cPiA"], "cPiA"],
        "./images/marker-icon.png": [["marker-icon.b29b8023.png", "tG0w"], "tG0w"]
    }], "f3z0": [function (require, module, exports) {
        var define;
        var global = arguments[3];
        var t, i = arguments[3];
        !function (i, e) {
            "object" == typeof exports && "undefined" != typeof module ? e(exports) : "function" == typeof t && t.amd ? t(["exports"], e) : e(i.L = {})
        }(this, function (t) {
            "use strict";

            function i(t) {
                var i, e, n, o;
                for (e = 1, n = arguments.length; e < n; e++) for (i in o = arguments[e]) t[i] = o[i];
                return t
            }

            var e = Object.create || function () {
                function t() {
                }

                return function (i) {
                    return t.prototype = i, new t
                }
            }();

            function n(t, i) {
                var e = Array.prototype.slice;
                if (t.bind) return t.bind.apply(t, e.call(arguments, 1));
                var n = e.call(arguments, 2);
                return function () {
                    return t.apply(i, n.length ? n.concat(e.call(arguments)) : arguments)
                }
            }

            var o = 0;

            function s(t) {
                try {
                    return t._leaflet_id = t._leaflet_id || ++o, t._leaflet_id
                } catch (e) {
                    
                }

            }

            function r(t, i, e) {
                var n, o, s, r;
                return r = function () {
                    n = !1, o && (s.apply(e, o), o = !1)
                }, s = function () {
                    n ? o = arguments : (t.apply(e, arguments), setTimeout(r, i), n = !0)
                }
            }

            function a(t, i, e) {
                var n = i[1], o = i[0], s = n - o;
                return t === n && e ? t : ((t - o) % s + s) % s + o
            }

            function h() {
                return !1
            }

            function u(t, i) {
                var e = Math.pow(10, void 0 === i ? 6 : i);
                return Math.round(t * e) / e
            }

            function l(t) {
                return t.trim ? t.trim() : t.replace(/^\s+|\s+$/g, "")
            }

            function c(t) {
                return l(t).split(/\s+/)
            }

            function _(t, i) {
                for (var n in Object.prototype.hasOwnProperty.call(t, "options") || (t.options = t.options ? e(t.options) : {}), i) t.options[n] = i[n];
                return t.options
            }

            function d(t, i, e) {
                var n = [];
                for (var o in t) n.push(encodeURIComponent(e ? o.toUpperCase() : o) + "=" + encodeURIComponent(t[o]));
                return (i && -1 !== i.indexOf("?") ? "&" : "?") + n.join("&")
            }

            var p = /\{ *([\w_-]+) *\}/g;

            function m(t, i) {
                return t.replace(p, function (t, e) {
                    var n = i[e];
                    if (void 0 === n) throw new Error("No value provided for variable " + t);
                    return "function" == typeof n && (n = n(i)), n
                })
            }

            var f = Array.isArray || function (t) {
                return "[object Array]" === Object.prototype.toString.call(t)
            };

            function g(t, i) {
                for (var e = 0; e < t.length; e++) if (t[e] === i) return e;
                return -1
            }

            var v = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";

            function y(t) {
                return window["webkit" + t] || window["moz" + t] || window["ms" + t]
            }

            var x = 0;

            function w(t) {
                var i = +new Date, e = Math.max(0, 16 - (i - x));
                return x = i + e, window.setTimeout(t, e)
            }

            var P = window.requestAnimationFrame || y("RequestAnimationFrame") || w,
                b = window.cancelAnimationFrame || y("CancelAnimationFrame") || y("CancelRequestAnimationFrame") || function (t) {
                    window.clearTimeout(t)
                };

            function T(t, i, e) {
                if (!e || P !== w) return P.call(window, n(t, i));
                t.call(i)
            }

            function M(t) {
                t && b.call(window, t)
            }

            var z = {
                extend: i,
                create: e,
                bind: n,
                lastId: o,
                stamp: s,
                throttle: r,
                wrapNum: a,
                falseFn: h,
                formatNum: u,
                trim: l,
                splitWords: c,
                setOptions: _,
                getParamString: d,
                template: m,
                isArray: f,
                indexOf: g,
                emptyImageUrl: v,
                requestFn: P,
                cancelFn: b,
                requestAnimFrame: T,
                cancelAnimFrame: M
            };

            function C() {
            }

            C.extend = function (t) {
                var n = function () {
                    this.initialize && this.initialize.apply(this, arguments), this.callInitHooks()
                }, o = n.__super__ = this.prototype, s = e(o);
                for (var r in s.constructor = n, n.prototype = s, this) Object.prototype.hasOwnProperty.call(this, r) && "prototype" !== r && "__super__" !== r && (n[r] = this[r]);
                return t.statics && (i(n, t.statics), delete t.statics), t.includes && (!function (t) {
                    if ("undefined" == typeof L || !L || !L.Mixin) return;
                    t = f(t) ? t : [t];
                    for (var i = 0; i < t.length; i++) t[i] === L.Mixin.Events && console.warn("Deprecated include of L.Mixin.Events: this property will be removed in future releases, please inherit from L.Evented instead.", (new Error).stack)
                }(t.includes), i.apply(null, [s].concat(t.includes)), delete t.includes), s.options && (t.options = i(e(s.options), t.options)), i(s, t), s._initHooks = [], s.callInitHooks = function () {
                    if (!this._initHooksCalled) {
                        o.callInitHooks && o.callInitHooks.call(this), this._initHooksCalled = !0;
                        for (var t = 0, i = s._initHooks.length; t < i; t++) s._initHooks[t].call(this)
                    }
                }, n
            }, C.include = function (t) {
                return i(this.prototype, t), this
            }, C.mergeOptions = function (t) {
                return i(this.prototype.options, t), this
            }, C.addInitHook = function (t) {
                var i = Array.prototype.slice.call(arguments, 1), e = "function" == typeof t ? t : function () {
                    this[t].apply(this, i)
                };
                return this.prototype._initHooks = this.prototype._initHooks || [], this.prototype._initHooks.push(e), this
            };
            var S = {
                on: function (t, i, e) {
                    if ("object" == typeof t) for (var n in t) this._on(n, t[n], i); else for (var o = 0, s = (t = c(t)).length; o < s; o++) this._on(t[o], i, e);
                    return this
                }, off: function (t, i, e) {
                    if (t) if ("object" == typeof t) for (var n in t) this._off(n, t[n], i); else for (var o = 0, s = (t = c(t)).length; o < s; o++) this._off(t[o], i, e); else delete this._events;
                    return this
                }, _on: function (t, i, e) {
                    this._events = this._events || {};
                    var n = this._events[t];
                    n || (n = [], this._events[t] = n), e === this && (e = void 0);
                    for (var o = {
                        fn: i,
                        ctx: e
                    }, s = n, r = 0, a = s.length; r < a; r++) if (s[r].fn === i && s[r].ctx === e) return;
                    s.push(o)
                }, _off: function (t, i, e) {
                    var n, o, s;
                    if (this._events && (n = this._events[t])) if (i) {
                        if (e === this && (e = void 0), n) for (o = 0, s = n.length; o < s; o++) {
                            var r = n[o];
                            if (r.ctx === e && r.fn === i) return r.fn = h, this._firingCount && (this._events[t] = n = n.slice()), void n.splice(o, 1)
                        }
                    } else {
                        for (o = 0, s = n.length; o < s; o++) n[o].fn = h;
                        delete this._events[t]
                    }
                }, fire: function (t, e, n) {
                    if (!this.listens(t, n)) return this;
                    var o = i({}, e, {type: t, target: this, sourceTarget: e && e.sourceTarget || this});
                    if (this._events) {
                        var s = this._events[t];
                        if (s) {
                            this._firingCount = this._firingCount + 1 || 1;
                            for (var r = 0, a = s.length; r < a; r++) {
                                var h = s[r];
                                h.fn.call(h.ctx || this, o)
                            }
                            this._firingCount--
                        }
                    }
                    return n && this._propagateEvent(o), this
                }, listens: function (t, i) {
                    var e = this._events && this._events[t];
                    if (e && e.length) return !0;
                    if (i) for (var n in this._eventParents) if (this._eventParents[n].listens(t, i)) return !0;
                    return !1
                }, once: function (t, i, e) {
                    if ("object" == typeof t) {
                        for (var o in t) this.once(o, t[o], i);
                        return this
                    }
                    var s = n(function () {
                        this.off(t, i, e).off(t, s, e)
                    }, this);
                    return this.on(t, i, e).on(t, s, e)
                }, addEventParent: function (t) {
                    return this._eventParents = this._eventParents || {}, this._eventParents[s(t)] = t, this
                }, removeEventParent: function (t) {
                    return this._eventParents && delete this._eventParents[s(t)], this
                }, _propagateEvent: function (t) {
                    for (var e in this._eventParents) this._eventParents[e].fire(t.type, i({
                        layer: t.target,
                        propagatedFrom: t.target
                    }, t), !0)
                }
            };
            S.addEventListener = S.on, S.removeEventListener = S.clearAllEventListeners = S.off, S.addOneTimeEventListener = S.once, S.fireEvent = S.fire, S.hasEventListeners = S.listens;
            var Z = C.extend(S);

            function E(t, i, e) {
                this.x = e ? Math.round(t) : t, this.y = e ? Math.round(i) : i
            }

            var k = Math.trunc || function (t) {
                return t > 0 ? Math.floor(t) : Math.ceil(t)
            };

            function B(t, i, e) {
                return t instanceof E ? t : f(t) ? new E(t[0], t[1]) : null == t ? t : "object" == typeof t && "x" in t && "y" in t ? new E(t.x, t.y) : new E(t, i, e)
            }

            function A(t, i) {
                if (t) for (var e = i ? [t, i] : t, n = 0, o = e.length; n < o; n++) this.extend(e[n])
            }

            function I(t, i) {
                return !t || t instanceof A ? t : new A(t, i)
            }

            function O(t, i) {
                if (t) for (var e = i ? [t, i] : t, n = 0, o = e.length; n < o; n++) this.extend(e[n])
            }

            function R(t, i) {
                return t instanceof O ? t : new O(t, i)
            }

            function N(t, i, e) {
                if (isNaN(t) || isNaN(i)) throw new Error("Invalid LatLng object: (" + t + ", " + i + ")");
                this.lat = +t, this.lng = +i, void 0 !== e && (this.alt = +e)
            }

            function D(t, i, e) {
                return t instanceof N ? t : f(t) && "object" != typeof t[0] ? 3 === t.length ? new N(t[0], t[1], t[2]) : 2 === t.length ? new N(t[0], t[1]) : null : null == t ? t : "object" == typeof t && "lat" in t ? new N(t.lat, "lng" in t ? t.lng : t.lon, t.alt) : void 0 === i ? null : new N(t, i, e)
            }

            E.prototype = {
                clone: function () {
                    return new E(this.x, this.y)
                }, add: function (t) {
                    return this.clone()._add(B(t))
                }, _add: function (t) {
                    return this.x += t.x, this.y += t.y, this
                }, subtract: function (t) {
                    return this.clone()._subtract(B(t))
                }, _subtract: function (t) {
                    return this.x -= t.x, this.y -= t.y, this
                }, divideBy: function (t) {
                    return this.clone()._divideBy(t)
                }, _divideBy: function (t) {
                    return this.x /= t, this.y /= t, this
                }, multiplyBy: function (t) {
                    return this.clone()._multiplyBy(t)
                }, _multiplyBy: function (t) {
                    return this.x *= t, this.y *= t, this
                }, scaleBy: function (t) {
                    return new E(this.x * t.x, this.y * t.y)
                }, unscaleBy: function (t) {
                    return new E(this.x / t.x, this.y / t.y)
                }, round: function () {
                    return this.clone()._round()
                }, _round: function () {
                    return this.x = Math.round(this.x), this.y = Math.round(this.y), this
                }, floor: function () {
                    return this.clone()._floor()
                }, _floor: function () {
                    return this.x = Math.floor(this.x), this.y = Math.floor(this.y), this
                }, ceil: function () {
                    return this.clone()._ceil()
                }, _ceil: function () {
                    return this.x = Math.ceil(this.x), this.y = Math.ceil(this.y), this
                }, trunc: function () {
                    return this.clone()._trunc()
                }, _trunc: function () {
                    return this.x = k(this.x), this.y = k(this.y), this
                }, distanceTo: function (t) {
                    var i = (t = B(t)).x - this.x, e = t.y - this.y;
                    return Math.sqrt(i * i + e * e)
                }, equals: function (t) {
                    return (t = B(t)).x === this.x && t.y === this.y
                }, contains: function (t) {
                    return t = B(t), Math.abs(t.x) <= Math.abs(this.x) && Math.abs(t.y) <= Math.abs(this.y)
                }, toString: function () {
                    return "Point(" + u(this.x) + ", " + u(this.y) + ")"
                }
            }, A.prototype = {
                extend: function (t) {
                    return t = B(t), this.min || this.max ? (this.min.x = Math.min(t.x, this.min.x), this.max.x = Math.max(t.x, this.max.x), this.min.y = Math.min(t.y, this.min.y), this.max.y = Math.max(t.y, this.max.y)) : (this.min = t.clone(), this.max = t.clone()), this
                }, getCenter: function (t) {
                    return new E((this.min.x + this.max.x) / 2, (this.min.y + this.max.y) / 2, t)
                }, getBottomLeft: function () {
                    return new E(this.min.x, this.max.y)
                }, getTopRight: function () {
                    return new E(this.max.x, this.min.y)
                }, getTopLeft: function () {
                    return this.min
                }, getBottomRight: function () {
                    return this.max
                }, getSize: function () {
                    return this.max.subtract(this.min)
                }, contains: function (t) {
                    var i, e;
                    return (t = "number" == typeof t[0] || t instanceof E ? B(t) : I(t)) instanceof A ? (i = t.min, e = t.max) : i = e = t, i.x >= this.min.x && e.x <= this.max.x && i.y >= this.min.y && e.y <= this.max.y
                }, intersects: function (t) {
                    t = I(t);
                    var i = this.min, e = this.max, n = t.min, o = t.max, s = o.x >= i.x && n.x <= e.x,
                        r = o.y >= i.y && n.y <= e.y;
                    return s && r
                }, overlaps: function (t) {
                    t = I(t);
                    var i = this.min, e = this.max, n = t.min, o = t.max, s = o.x > i.x && n.x < e.x,
                        r = o.y > i.y && n.y < e.y;
                    return s && r
                }, isValid: function () {
                    return !(!this.min || !this.max)
                }
            }, O.prototype = {
                extend: function (t) {
                    var i, e, n = this._southWest, o = this._northEast;
                    if (t instanceof N) i = t, e = t; else {
                        if (!(t instanceof O)) return t ? this.extend(D(t) || R(t)) : this;
                        if (i = t._southWest, e = t._northEast, !i || !e) return this
                    }
                    return n || o ? (n.lat = Math.min(i.lat, n.lat), n.lng = Math.min(i.lng, n.lng), o.lat = Math.max(e.lat, o.lat), o.lng = Math.max(e.lng, o.lng)) : (this._southWest = new N(i.lat, i.lng), this._northEast = new N(e.lat, e.lng)), this
                }, pad: function (t) {
                    var i = this._southWest, e = this._northEast, n = Math.abs(i.lat - e.lat) * t,
                        o = Math.abs(i.lng - e.lng) * t;
                    return new O(new N(i.lat - n, i.lng - o), new N(e.lat + n, e.lng + o))
                }, getCenter: function () {
                    return new N((this._southWest.lat + this._northEast.lat) / 2, (this._southWest.lng + this._northEast.lng) / 2)
                }, getSouthWest: function () {
                    return this._southWest
                }, getNorthEast: function () {
                    return this._northEast
                }, getNorthWest: function () {
                    return new N(this.getNorth(), this.getWest())
                }, getSouthEast: function () {
                    return new N(this.getSouth(), this.getEast())
                }, getWest: function () {
                    return this._southWest.lng
                }, getSouth: function () {
                    return this._southWest.lat
                }, getEast: function () {
                    return this._northEast.lng
                }, getNorth: function () {
                    return this._northEast.lat
                }, contains: function (t) {
                    t = "number" == typeof t[0] || t instanceof N || "lat" in t ? D(t) : R(t);
                    var i, e, n = this._southWest, o = this._northEast;
                    return t instanceof O ? (i = t.getSouthWest(), e = t.getNorthEast()) : i = e = t, i.lat >= n.lat && e.lat <= o.lat && i.lng >= n.lng && e.lng <= o.lng
                }, intersects: function (t) {
                    t = R(t);
                    var i = this._southWest, e = this._northEast, n = t.getSouthWest(), o = t.getNorthEast(),
                        s = o.lat >= i.lat && n.lat <= e.lat, r = o.lng >= i.lng && n.lng <= e.lng;
                    return s && r
                }, overlaps: function (t) {
                    t = R(t);
                    var i = this._southWest, e = this._northEast, n = t.getSouthWest(), o = t.getNorthEast(),
                        s = o.lat > i.lat && n.lat < e.lat, r = o.lng > i.lng && n.lng < e.lng;
                    return s && r
                }, toBBoxString: function () {
                    return [this.getWest(), this.getSouth(), this.getEast(), this.getNorth()].join(",")
                }, equals: function (t, i) {
                    return !!t && (t = R(t), this._southWest.equals(t.getSouthWest(), i) && this._northEast.equals(t.getNorthEast(), i))
                }, isValid: function () {
                    return !(!this._southWest || !this._northEast)
                }
            }, N.prototype = {
                equals: function (t, i) {
                    return !!t && (t = D(t), Math.max(Math.abs(this.lat - t.lat), Math.abs(this.lng - t.lng)) <= (void 0 === i ? 1e-9 : i))
                }, toString: function (t) {
                    return "LatLng(" + u(this.lat, t) + ", " + u(this.lng, t) + ")"
                }, distanceTo: function (t) {
                    return H.distance(this, D(t))
                }, wrap: function () {
                    return H.wrapLatLng(this)
                }, toBounds: function (t) {
                    var i = 180 * t / 40075017, e = i / Math.cos(Math.PI / 180 * this.lat);
                    return R([this.lat - i, this.lng - e], [this.lat + i, this.lng + e])
                }, clone: function () {
                    return new N(this.lat, this.lng, this.alt)
                }
            };
            var j, W = {
                latLngToPoint: function (t, i) {
                    var e = this.projection.project(t), n = this.scale(i);
                    return this.transformation._transform(e, n)
                }, pointToLatLng: function (t, i) {
                    var e = this.scale(i), n = this.transformation.untransform(t, e);
                    return this.projection.unproject(n)
                }, project: function (t) {
                    return this.projection.project(t)
                }, unproject: function (t) {
                    return this.projection.unproject(t)
                }, scale: function (t) {
                    return 256 * Math.pow(2, t)
                }, zoom: function (t) {
                    return Math.log(t / 256) / Math.LN2
                }, getProjectedBounds: function (t) {
                    if (this.infinite) return null;
                    var i = this.projection.bounds, e = this.scale(t);
                    return new A(this.transformation.transform(i.min, e), this.transformation.transform(i.max, e))
                }, infinite: !1, wrapLatLng: function (t) {
                    var i = this.wrapLng ? a(t.lng, this.wrapLng, !0) : t.lng;
                    return new N(this.wrapLat ? a(t.lat, this.wrapLat, !0) : t.lat, i, t.alt)
                }, wrapLatLngBounds: function (t) {
                    var i = t.getCenter(), e = this.wrapLatLng(i), n = i.lat - e.lat, o = i.lng - e.lng;
                    if (0 === n && 0 === o) return t;
                    var s = t.getSouthWest(), r = t.getNorthEast();
                    return new O(new N(s.lat - n, s.lng - o), new N(r.lat - n, r.lng - o))
                }
            }, H = i({}, W, {
                wrapLng: [-180, 180], R: 6371e3, distance: function (t, i) {
                    var e = Math.PI / 180, n = t.lat * e, o = i.lat * e, s = Math.sin((i.lat - t.lat) * e / 2),
                        r = Math.sin((i.lng - t.lng) * e / 2), a = s * s + Math.cos(n) * Math.cos(o) * r * r,
                        h = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
                    return this.R * h
                }
            }), F = {
                R: 6378137, MAX_LATITUDE: 85.0511287798, project: function (t) {
                    var i = Math.PI / 180, e = this.MAX_LATITUDE, n = Math.max(Math.min(e, t.lat), -e),
                        o = Math.sin(n * i);
                    return new E(this.R * t.lng * i, this.R * Math.log((1 + o) / (1 - o)) / 2)
                }, unproject: function (t) {
                    var i = 180 / Math.PI;
                    return new N((2 * Math.atan(Math.exp(t.y / this.R)) - Math.PI / 2) * i, t.x * i / this.R)
                }, bounds: (j = 6378137 * Math.PI, new A([-j, -j], [j, j]))
            };

            function U(t, i, e, n) {
                if (f(t)) return this._a = t[0], this._b = t[1], this._c = t[2], void (this._d = t[3]);
                this._a = t, this._b = i, this._c = e, this._d = n
            }

            function V(t, i, e, n) {
                return new U(t, i, e, n)
            }

            U.prototype = {
                transform: function (t, i) {
                    return this._transform(t.clone(), i)
                }, _transform: function (t, i) {
                    return i = i || 1, t.x = i * (this._a * t.x + this._b), t.y = i * (this._c * t.y + this._d), t
                }, untransform: function (t, i) {
                    return i = i || 1, new E((t.x / i - this._b) / this._a, (t.y / i - this._d) / this._c)
                }
            };
            var q = i({}, H, {
                code: "EPSG:3857", projection: F, transformation: function () {
                    var t = .5 / (Math.PI * F.R);
                    return V(t, .5, -t, .5)
                }()
            }), G = i({}, q, {code: "EPSG:900913"});

            function K(t) {
                return document.createElementNS("http://www.w3.org/2000/svg", t)
            }

            function Y(t, i) {
                var e, n, o, s, r, a, h = "";
                for (e = 0, o = t.length; e < o; e++) {
                    for (n = 0, s = (r = t[e]).length; n < s; n++) h += (n ? "L" : "M") + (a = r[n]).x + " " + a.y;
                    h += i ? zt ? "z" : "x" : ""
                }
                return h || "M0 0"
            }

            var X = document.documentElement.style, J = "ActiveXObject" in window, $ = J && !document.addEventListener,
                Q = "msLaunchUri" in navigator && !("documentMode" in document), tt = St("webkit"), it = St("android"),
                et = St("android 2") || St("android 3"),
                nt = parseInt(/WebKit\/([0-9]+)|$/.exec(navigator.userAgent)[1], 10),
                ot = it && St("Google") && nt < 537 && !("AudioNode" in window), st = !!window.opera,
                rt = !Q && St("chrome"), at = St("gecko") && !tt && !st && !J, ht = !rt && St("safari"),
                ut = St("phantom"), lt = "OTransition" in X, ct = 0 === navigator.platform.indexOf("Win"),
                _t = J && "transition" in X,
                dt = "WebKitCSSMatrix" in window && "m11" in new window.WebKitCSSMatrix && !et,
                pt = "MozPerspective" in X, mt = !window.L_DISABLE_3D && (_t || dt || pt) && !lt && !ut,
                ft = "undefined" != typeof orientation || St("mobile"), gt = ft && tt, vt = ft && dt,
                yt = !window.PointerEvent && window.MSPointerEvent, xt = !(!window.PointerEvent && !yt),
                wt = !window.L_NO_TOUCH && (xt || "ontouchstart" in window || window.DocumentTouch && document instanceof window.DocumentTouch),
                Pt = ft && st, Lt = ft && at,
                bt = (window.devicePixelRatio || window.screen.deviceXDPI / window.screen.logicalXDPI) > 1,
                Tt = function () {
                    var t = !1;
                    try {
                        var i = Object.defineProperty({}, "passive", {
                            get: function () {
                                t = !0
                            }
                        });
                        window.addEventListener("testPassiveEventSupport", h, i), window.removeEventListener("testPassiveEventSupport", h, i)
                    } catch (e) {
                    }
                    return t
                }(), Mt = !!document.createElement("canvas").getContext,
                zt = !(!document.createElementNS || !K("svg").createSVGRect), Ct = !zt && function () {
                    try {
                        var t = document.createElement("div");
                        t.innerHTML = '<v:shape adj="1"/>';
                        var i = t.firstChild;
                        return i.style.behavior = "url(#default#VML)", i && "object" == typeof i.adj
                    } catch (e) {
                        return !1
                    }
                }();

            function St(t) {
                return navigator.userAgent.toLowerCase().indexOf(t) >= 0
            }

            var Zt = {
                    ie: J,
                    ielt9: $,
                    edge: Q,
                    webkit: tt,
                    android: it,
                    android23: et,
                    androidStock: ot,
                    opera: st,
                    chrome: rt,
                    gecko: at,
                    safari: ht,
                    phantom: ut,
                    opera12: lt,
                    win: ct,
                    ie3d: _t,
                    webkit3d: dt,
                    gecko3d: pt,
                    any3d: mt,
                    mobile: ft,
                    mobileWebkit: gt,
                    mobileWebkit3d: vt,
                    msPointer: yt,
                    pointer: xt,
                    touch: wt,
                    mobileOpera: Pt,
                    mobileGecko: Lt,
                    retina: bt,
                    passiveEvents: Tt,
                    canvas: Mt,
                    svg: zt,
                    vml: Ct
                }, Et = yt ? "MSPointerDown" : "pointerdown", kt = yt ? "MSPointerMove" : "pointermove",
                Bt = yt ? "MSPointerUp" : "pointerup", At = yt ? "MSPointerCancel" : "pointercancel", It = {}, Ot = !1;

            function Rt(t, i, e, o) {
                return "touchstart" === i ? function (t, i, e) {
                    var o = n(function (t) {
                        t.MSPOINTER_TYPE_TOUCH && t.pointerType === t.MSPOINTER_TYPE_TOUCH && Ai(t), Wt(t, i)
                    });
                    t["_leaflet_touchstart" + e] = o, t.addEventListener(Et, o, !1), Ot || (document.addEventListener(Et, Nt, !0), document.addEventListener(kt, Dt, !0), document.addEventListener(Bt, jt, !0), document.addEventListener(At, jt, !0), Ot = !0)
                }(t, e, o) : "touchmove" === i ? function (t, i, e) {
                    var n = function (t) {
                        t.pointerType === (t.MSPOINTER_TYPE_MOUSE || "mouse") && 0 === t.buttons || Wt(t, i)
                    };
                    t["_leaflet_touchmove" + e] = n, t.addEventListener(kt, n, !1)
                }(t, e, o) : "touchend" === i && function (t, i, e) {
                    var n = function (t) {
                        Wt(t, i)
                    };
                    t["_leaflet_touchend" + e] = n, t.addEventListener(Bt, n, !1), t.addEventListener(At, n, !1)
                }(t, e, o), this
            }

            function Nt(t) {
                It[t.pointerId] = t
            }

            function Dt(t) {
                It[t.pointerId] && (It[t.pointerId] = t)
            }

            function jt(t) {
                delete It[t.pointerId]
            }

            function Wt(t, i) {
                for (var e in t.touches = [], It) t.touches.push(It[e]);
                t.changedTouches = [t], i(t)
            }

            var Ht = yt ? "MSPointerDown" : xt ? "pointerdown" : "touchstart",
                Ft = yt ? "MSPointerUp" : xt ? "pointerup" : "touchend", Ut = "_leaflet_";
            var Vt, qt, Gt, Kt, Yt,
                Xt = _i(["transform", "webkitTransform", "OTransform", "MozTransform", "msTransform"]),
                Jt = _i(["webkitTransition", "transition", "OTransition", "MozTransition", "msTransition"]),
                $t = "webkitTransition" === Jt || "OTransition" === Jt ? Jt + "End" : "transitionend";

            function Qt(t) {
                return "string" == typeof t ? document.getElementById(t) : t
            }

            function ti(t, i) {
                try {
                    var e = t.style[i] || t.currentStyle && t.currentStyle[i];
                    if ((!e || "auto" === e) && document.defaultView) {
                        var n = document.defaultView.getComputedStyle(t, null);
                        e = n ? n[i] : null
                    }
                    return "auto" === e ? null : e
                } catch (e) {
                }

            }

            function ii(t, i, e) {
                var n = document.createElement(t);
                return n.className = i || "", e && e.appendChild(n), n
            }

            function ei(t) {
                var i = t.parentNode;
                i && i.removeChild(t)
            }

            function ni(t) {
                for (; t.firstChild;) t.removeChild(t.firstChild)
            }

            function oi(t) {
                var i = t.parentNode;
                i && i.lastChild !== t && i.appendChild(t)
            }

            function si(t) {
                var i = t.parentNode;
                i && i.firstChild !== t && i.insertBefore(t, i.firstChild)
            }

            function ri(t, i) {
                if (void 0 !== t.classList) return t.classList.contains(i);
                var e = li(t);
                return e.length > 0 && new RegExp("(^|\\s)" + i + "(\\s|$)").test(e)
            }

            function ai(t, i) {
                try {
                    if (void 0 !== t.classList) for (var e = c(i), n = 0, o = e.length; n < o; n++) t.classList.add(e[n]); else if (!ri(t, i)) {
                        var s = li(t);
                        ui(t, (s ? s + " " : "") + i)
                    }
                } catch (e) {
                    
                }

            }

            function hi(t, i) {
                void 0 !== t.classList ? t.classList.remove(i) : ui(t, l((" " + li(t) + " ").replace(" " + i + " ", " ")))
            }

            function ui(t, i) {
                void 0 === t.className.baseVal ? t.className = i : t.className.baseVal = i
            }

            function li(t) {
                return t.correspondingElement && (t = t.correspondingElement), void 0 === t.className.baseVal ? t.className : t.className.baseVal
            }

            function ci(t, i) {
                "opacity" in t.style ? t.style.opacity = i : "filter" in t.style && function (t, i) {
                    var e = !1, n = "DXImageTransform.Microsoft.Alpha";
                    try {
                        e = t.filters.item(n)
                    } catch (o) {
                        if (1 === i) return
                    }
                    i = Math.round(100 * i), e ? (e.Enabled = 100 !== i, e.Opacity = i) : t.style.filter += " progid:" + n + "(opacity=" + i + ")"
                }(t, i)
            }

            function _i(t) {
                for (var i = document.documentElement.style, e = 0; e < t.length; e++) if (t[e] in i) return t[e];
                return !1
            }

            function di(t, i, e) {
                var n = i || new E(0, 0);
                t.style[Xt] = (_t ? "translate(" + n.x + "px," + n.y + "px)" : "translate3d(" + n.x + "px," + n.y + "px,0)") + (e ? " scale(" + e + ")" : "")
            }

            function pi(t, i) {
                try {
                    t._leaflet_pos = i, mt ? di(t, i) : (t.style.left = i.x + "px", t.style.top = i.y + "px")
                }catch (e) {
                    
                }

            }

            function mi(t) {
                try {
                    return t._leaflet_pos || new E(0, 0)
                }catch (e) {

                }

            }

            if ("onselectstart" in document) Vt = function () {
                bi(window, "selectstart", Ai)
            }, qt = function () {
                Mi(window, "selectstart", Ai)
            }; else {
                var fi = _i(["userSelect", "WebkitUserSelect", "OUserSelect", "MozUserSelect", "msUserSelect"]);
                Vt = function () {
                    if (fi) {
                        var t = document.documentElement.style;
                        Gt = t[fi], t[fi] = "none"
                    }
                }, qt = function () {
                    fi && (document.documentElement.style[fi] = Gt, Gt = void 0)
                }
            }

            function gi() {
                bi(window, "dragstart", Ai)
            }

            function vi() {
                Mi(window, "dragstart", Ai)
            }

            function yi(t) {
                for (; -1 === t.tabIndex;) t = t.parentNode;
                t.style && (xi(), Kt = t, Yt = t.style.outline, t.style.outline = "none", bi(window, "keydown", xi))
            }

            function xi() {
                Kt && (Kt.style.outline = Yt, Kt = void 0, Yt = void 0, Mi(window, "keydown", xi))
            }

            function wi(t) {
                do {
                    t = t.parentNode
                } while (!(t.offsetWidth && t.offsetHeight || t === document.body));
                return t
            }

            function Pi(t) {
                var i = t.getBoundingClientRect();
                return {x: i.width / t.offsetWidth || 1, y: i.height / t.offsetHeight || 1, boundingClientRect: i}
            }

            var Li = {
                TRANSFORM: Xt,
                TRANSITION: Jt,
                TRANSITION_END: $t,
                get: Qt,
                getStyle: ti,
                create: ii,
                remove: ei,
                empty: ni,
                toFront: oi,
                toBack: si,
                hasClass: ri,
                addClass: ai,
                removeClass: hi,
                setClass: ui,
                getClass: li,
                setOpacity: ci,
                testProp: _i,
                setTransform: di,
                setPosition: pi,
                getPosition: mi,
                disableTextSelection: Vt,
                enableTextSelection: qt,
                disableImageDrag: gi,
                enableImageDrag: vi,
                preventOutline: yi,
                restoreOutline: xi,
                getSizedParentNode: wi,
                getScale: Pi
            };

            function bi(t, i, e, n) {
                if ("object" == typeof i) for (var o in i) Si(t, o, i[o], e); else for (var s = 0, r = (i = c(i)).length; s < r; s++) Si(t, i[s], e, n);
                return this
            }

            var Ti = "_leaflet_events";

            function Mi(t, i, e, n) {
                if ("object" == typeof i) for (var o in i) Zi(t, o, i[o], e); else if (i) for (var s = 0, r = (i = c(i)).length; s < r; s++) Zi(t, i[s], e, n); else {
                    for (var a in t[Ti]) Zi(t, a, t[Ti][a]);
                    delete t[Ti]
                }
                return this
            }

            function zi() {
                if (xt) return !(Q || ht)
            }

            var Ci = {mouseenter: "mouseover", mouseleave: "mouseout", wheel: !("onwheel" in window) && "mousewheel"};

            function Si(t, i, e, n) {
                try {
                    var o = i + s(e) + (n ? "_" + s(n) : "");
                    if (t[Ti] && t[Ti][o]) return this;
                    var r = function (i) {
                        return e.call(n || t, i || window.event)
                    }, a = r;
                    xt && 0 === i.indexOf("touch") ? Rt(t, i, r, o) : wt && "dblclick" === i && !zi() ? function (t, i, e) {
                        var n, o, s = !1, r = 250;

                        function a(t) {
                            if (xt) {
                                if (!t.isPrimary) return;
                                if ("mouse" === t.pointerType) return
                            } else if (t.touches.length > 1) return;
                            var i = Date.now(), e = i - (n || i);
                            o = t.touches ? t.touches[0] : t, s = e > 0 && e <= r, n = i
                        }

                        function h(t) {
                            if (s && !o.cancelBubble) {
                                if (xt) {
                                    if ("mouse" === t.pointerType) return;
                                    var e, r, a = {};
                                    for (r in o) e = o[r], a[r] = e && e.bind ? e.bind(o) : e;
                                    o = a
                                }
                                o.type = "dblclick", o.button = 0, i(o), n = null
                            }
                        }

                        t[Ut + Ht + e] = a, t[Ut + Ft + e] = h, t[Ut + "dblclick" + e] = i, t.addEventListener(Ht, a, !!Tt && {passive: !1}), t.addEventListener(Ft, h, !!Tt && {passive: !1}), t.addEventListener("dblclick", i, !1)
                    }(t, r, o) : "addEventListener" in t ? "touchstart" === i || "touchmove" === i || "wheel" === i || "mousewheel" === i ? t.addEventListener(Ci[i] || i, r, !!Tt && {passive: !1}) : "mouseenter" === i || "mouseleave" === i ? (r = function (i) {
                        i = i || window.event, Hi(t, i) && a(i)
                    }, t.addEventListener(Ci[i], r, !1)) : t.addEventListener(i, a, !1) : "attachEvent" in t && t.attachEvent("on" + i, r), t[Ti] = t[Ti] || {}, t[Ti][o] = r
                } catch (e) {
                    
                }

            }

            function Zi(t, i, e, n) {
                var o = i + s(e) + (n ? "_" + s(n) : ""), r = t[Ti] && t[Ti][o];
                if (!r) return this;
                xt && 0 === i.indexOf("touch") ? function (t, i, e) {
                    var n = t["_leaflet_" + i + e];
                    "touchstart" === i ? t.removeEventListener(Et, n, !1) : "touchmove" === i ? t.removeEventListener(kt, n, !1) : "touchend" === i && (t.removeEventListener(Bt, n, !1), t.removeEventListener(At, n, !1))
                }(t, i, o) : wt && "dblclick" === i && !zi() ? function (t, i) {
                    var e = t[Ut + Ht + i], n = t[Ut + Ft + i], o = t[Ut + "dblclick" + i];
                    t.removeEventListener(Ht, e, !!Tt && {passive: !1}), t.removeEventListener(Ft, n, !!Tt && {passive: !1}), t.removeEventListener("dblclick", o, !1)
                }(t, o) : "removeEventListener" in t ? t.removeEventListener(Ci[i] || i, r, !1) : "detachEvent" in t && t.detachEvent("on" + i, r), t[Ti][o] = null
            }

            function Ei(t) {
                return t.stopPropagation ? t.stopPropagation() : t.originalEvent ? t.originalEvent._stopped = !0 : t.cancelBubble = !0, Wi(t), this
            }

            function ki(t) {
                return Si(t, "wheel", Ei), this
            }

            function Bi(t) {
                return bi(t, "mousedown touchstart dblclick", Ei), Si(t, "click", ji), this
            }

            function Ai(t) {
                return t.preventDefault ? t.preventDefault() : t.returnValue = !1, this
            }

            function Ii(t) {
                return Ai(t), Ei(t), this
            }

            function Oi(t, i) {
                if (!i) return new E(t.clientX, t.clientY);
                var e = Pi(i), n = e.boundingClientRect;
                return new E((t.clientX - n.left) / e.x - i.clientLeft, (t.clientY - n.top) / e.y - i.clientTop)
            }

            var Ri = ct && rt ? 2 * window.devicePixelRatio : at ? window.devicePixelRatio : 1;

            function Ni(t) {
                return Q ? t.wheelDeltaY / 2 : t.deltaY && 0 === t.deltaMode ? -t.deltaY / Ri : t.deltaY && 1 === t.deltaMode ? 20 * -t.deltaY : t.deltaY && 2 === t.deltaMode ? 60 * -t.deltaY : t.deltaX || t.deltaZ ? 0 : t.wheelDelta ? (t.wheelDeltaY || t.wheelDelta) / 2 : t.detail && Math.abs(t.detail) < 32765 ? 20 * -t.detail : t.detail ? t.detail / -32765 * 60 : 0
            }

            var Di = {};

            function ji(t) {
                Di[t.type] = !0
            }

            function Wi(t) {
                var i = Di[t.type];
                return Di[t.type] = !1, i
            }

            function Hi(t, i) {
                var e = i.relatedTarget;
                if (!e) return !0;
                try {
                    for (; e && e !== t;) e = e.parentNode
                } catch (n) {
                    return !1
                }
                return e !== t
            }

            var Fi = {
                on: bi,
                off: Mi,
                stopPropagation: Ei,
                disableScrollPropagation: ki,
                disableClickPropagation: Bi,
                preventDefault: Ai,
                stop: Ii,
                getMousePosition: Oi,
                getWheelDelta: Ni,
                fakeStop: ji,
                skipped: Wi,
                isExternalTarget: Hi,
                addListener: bi,
                removeListener: Mi
            }, Ui = Z.extend({
                run: function (t, i, e, n) {
                    this.stop(), this._el = t, this._inProgress = !0, this._duration = e || .25, this._easeOutPower = 1 / Math.max(n || .5, .2), this._startPos = mi(t), this._offset = i.subtract(this._startPos), this._startTime = +new Date, this.fire("start"), this._animate()
                }, stop: function () {
                    this._inProgress && (this._step(!0), this._complete())
                }, _animate: function () {
                    this._animId = T(this._animate, this), this._step()
                }, _step: function (t) {
                    var i = +new Date - this._startTime, e = 1e3 * this._duration;
                    i < e ? this._runFrame(this._easeOut(i / e), t) : (this._runFrame(1), this._complete())
                }, _runFrame: function (t, i) {
                    var e = this._startPos.add(this._offset.multiplyBy(t));
                    i && e._round(), pi(this._el, e), this.fire("step")
                }, _complete: function () {
                    M(this._animId), this._inProgress = !1, this.fire("end")
                }, _easeOut: function (t) {
                    return 1 - Math.pow(1 - t, this._easeOutPower)
                }
            }), Vi = Z.extend({
                options: {
                    crs: q,
                    center: void 0,
                    zoom: void 0,
                    minZoom: void 0,
                    maxZoom: void 0,
                    layers: [],
                    maxBounds: void 0,
                    renderer: void 0,
                    zoomAnimation: !0,
                    zoomAnimationThreshold: 4,
                    fadeAnimation: !0,
                    markerZoomAnimation: !0,
                    transform3DLimit: 8388608,
                    zoomSnap: 1,
                    zoomDelta: 1,
                    trackResize: !0
                },
                initialize: function (t, i) {
                    i = _(this, i), this._handlers = [], this._layers = {}, this._zoomBoundLayers = {}, this._sizeChanged = !0, this._initContainer(t), this._initLayout(), this._onResize = n(this._onResize, this), this._initEvents(), i.maxBounds && this.setMaxBounds(i.maxBounds), void 0 !== i.zoom && (this._zoom = this._limitZoom(i.zoom)), i.center && void 0 !== i.zoom && this.setView(D(i.center), i.zoom, {reset: !0}), this.callInitHooks(), this._zoomAnimated = Jt && mt && !Pt && this.options.zoomAnimation, this._zoomAnimated && (this._createAnimProxy(), bi(this._proxy, $t, this._catchTransitionEnd, this)), this._addLayers(this.options.layers)
                },
                setView: function (t, e, n) {
                    if ((e = void 0 === e ? this._zoom : this._limitZoom(e), t = this._limitCenter(D(t), e, this.options.maxBounds), n = n || {}, this._stop(), this._loaded && !n.reset && !0 !== n) && (void 0 !== n.animate && (n.zoom = i({animate: n.animate}, n.zoom), n.pan = i({
                        animate: n.animate,
                        duration: n.duration
                    }, n.pan)), this._zoom !== e ? this._tryAnimatedZoom && this._tryAnimatedZoom(t, e, n.zoom) : this._tryAnimatedPan(t, n.pan))) return clearTimeout(this._sizeTimer), this;
                    return this._resetView(t, e), this
                },
                setZoom: function (t, i) {
                    return this._loaded ? this.setView(this.getCenter(), t, {zoom: i}) : (this._zoom = t, this)
                },
                zoomIn: function (t, i) {
                    return t = t || (mt ? this.options.zoomDelta : 1), this.setZoom(this._zoom + t, i)
                },
                zoomOut: function (t, i) {
                    return t = t || (mt ? this.options.zoomDelta : 1), this.setZoom(this._zoom - t, i)
                },
                setZoomAround: function (t, i, e) {
                    var n = this.getZoomScale(i), o = this.getSize().divideBy(2),
                        s = (t instanceof E ? t : this.latLngToContainerPoint(t)).subtract(o).multiplyBy(1 - 1 / n),
                        r = this.containerPointToLatLng(o.add(s));
                    return this.setView(r, i, {zoom: e})
                },
                _getBoundsCenterZoom: function (t, i) {
                    i = i || {}, t = t.getBounds ? t.getBounds() : R(t);
                    var e = B(i.paddingTopLeft || i.padding || [0, 0]),
                        n = B(i.paddingBottomRight || i.padding || [0, 0]), o = this.getBoundsZoom(t, !1, e.add(n));
                    if ((o = "number" == typeof i.maxZoom ? Math.min(i.maxZoom, o) : o) === 1 / 0) return {
                        center: t.getCenter(),
                        zoom: o
                    };
                    var s = n.subtract(e).divideBy(2), r = this.project(t.getSouthWest(), o),
                        a = this.project(t.getNorthEast(), o);
                    return {center: this.unproject(r.add(a).divideBy(2).add(s), o), zoom: o}
                },
                fitBounds: function (t, i) {
                    if (!(t = R(t)).isValid()) throw new Error("Bounds are not valid.");
                    var e = this._getBoundsCenterZoom(t, i);
                    return this.setView(e.center, e.zoom, i)
                },
                fitWorld: function (t) {
                    return this.fitBounds([[-90, -180], [90, 180]], t)
                },
                panTo: function (t, i) {
                    return this.setView(t, this._zoom, {pan: i})
                },
                panBy: function (t, i) {
                    if (i = i || {}, !(t = B(t).round()).x && !t.y) return this.fire("moveend");
                    if (!0 !== i.animate && !this.getSize().contains(t)) return this._resetView(this.unproject(this.project(this.getCenter()).add(t)), this.getZoom()), this;
                    if (this._panAnim || (this._panAnim = new Ui, this._panAnim.on({
                        step: this._onPanTransitionStep,
                        end: this._onPanTransitionEnd
                    }, this)), i.noMoveStart || this.fire("movestart"), !1 !== i.animate) {
                        ai(this._mapPane, "leaflet-pan-anim");
                        var e = this._getMapPanePos().subtract(t).round();
                        this._panAnim.run(this._mapPane, e, i.duration || .25, i.easeLinearity)
                    } else this._rawPanBy(t), this.fire("move").fire("moveend");
                    return this
                },
                flyTo: function (t, i, e) {
                    if (!1 === (e = e || {}).animate || !mt) return this.setView(t, i, e);
                    this._stop();
                    var n = this.project(this.getCenter()), o = this.project(t), s = this.getSize(), r = this._zoom;
                    t = D(t), i = void 0 === i ? r : i;
                    var a = Math.max(s.x, s.y), h = a * this.getZoomScale(r, i), u = o.distanceTo(n) || 1, l = 1.42,
                        c = l * l;

                    function _(t) {
                        var i = (h * h - a * a + (t ? -1 : 1) * c * c * u * u) / (2 * (t ? h : a) * c * u),
                            e = Math.sqrt(i * i + 1) - i;
                        return e < 1e-9 ? -18 : Math.log(e)
                    }

                    function d(t) {
                        return (Math.exp(t) - Math.exp(-t)) / 2
                    }

                    function p(t) {
                        return (Math.exp(t) + Math.exp(-t)) / 2
                    }

                    var m = _(0);

                    function f(t) {
                        return a * (p(m) * (d(i = m + l * t) / p(i)) - d(m)) / c;
                        var i
                    }

                    var g = Date.now(), v = (_(1) - m) / l, y = e.duration ? 1e3 * e.duration : 1e3 * v * .8;
                    return this._moveStart(!0, e.noMoveStart), function e() {
                        var s = (Date.now() - g) / y, h = function (t) {
                            return 1 - Math.pow(1 - t, 1.5)
                        }(s) * v;
                        s <= 1 ? (this._flyToFrame = T(e, this), this._move(this.unproject(n.add(o.subtract(n).multiplyBy(f(h) / u)), r), this.getScaleZoom(a / function (t) {
                            return a * (p(m) / p(m + l * t))
                        }(h), r), {flyTo: !0})) : this._move(t, i)._moveEnd(!0)
                    }.call(this), this
                },
                flyToBounds: function (t, i) {
                    var e = this._getBoundsCenterZoom(t, i);
                    return this.flyTo(e.center, e.zoom, i)
                },
                setMaxBounds: function (t) {
                    return (t = R(t)).isValid() ? (this.options.maxBounds && this.off("moveend", this._panInsideMaxBounds), this.options.maxBounds = t, this._loaded && this._panInsideMaxBounds(), this.on("moveend", this._panInsideMaxBounds)) : (this.options.maxBounds = null, this.off("moveend", this._panInsideMaxBounds))
                },
                setMinZoom: function (t) {
                    var i = this.options.minZoom;
                    return this.options.minZoom = t, this._loaded && i !== t && (this.fire("zoomlevelschange"), this.getZoom() < this.options.minZoom) ? this.setZoom(t) : this
                },
                setMaxZoom: function (t) {
                    var i = this.options.maxZoom;
                    return this.options.maxZoom = t, this._loaded && i !== t && (this.fire("zoomlevelschange"), this.getZoom() > this.options.maxZoom) ? this.setZoom(t) : this
                },
                panInsideBounds: function (t, i) {
                    this._enforcingBounds = !0;
                    var e = this.getCenter(), n = this._limitCenter(e, this._zoom, R(t));
                    return e.equals(n) || this.panTo(n, i), this._enforcingBounds = !1, this
                },
                panInside: function (t, i) {
                    var e = B((i = i || {}).paddingTopLeft || i.padding || [0, 0]),
                        n = B(i.paddingBottomRight || i.padding || [0, 0]), o = this.getCenter(), s = this.project(o),
                        r = this.project(t), a = this.getPixelBounds(), h = a.getSize().divideBy(2),
                        u = I([a.min.add(e), a.max.subtract(n)]);
                    if (!u.contains(r)) {
                        this._enforcingBounds = !0;
                        var l = s.subtract(r), c = B(r.x + l.x, r.y + l.y);
                        (r.x < u.min.x || r.x > u.max.x) && (c.x = s.x - l.x, l.x > 0 ? c.x += h.x - e.x : c.x -= h.x - n.x), (r.y < u.min.y || r.y > u.max.y) && (c.y = s.y - l.y, l.y > 0 ? c.y += h.y - e.y : c.y -= h.y - n.y), this.panTo(this.unproject(c), i), this._enforcingBounds = !1
                    }
                    return this
                },
                invalidateSize: function (t) {
                    if (!this._loaded) return this;
                    t = i({animate: !1, pan: !0}, !0 === t ? {animate: !0} : t);
                    var e = this.getSize();
                    this._sizeChanged = !0, this._lastCenter = null;
                    var o = this.getSize(), s = e.divideBy(2).round(), r = o.divideBy(2).round(), a = s.subtract(r);
                    return a.x || a.y ? (t.animate && t.pan ? this.panBy(a) : (t.pan && this._rawPanBy(a), this.fire("move"), t.debounceMoveend ? (clearTimeout(this._sizeTimer), this._sizeTimer = setTimeout(n(this.fire, this, "moveend"), 200)) : this.fire("moveend")), this.fire("resize", {
                        oldSize: e,
                        newSize: o
                    })) : this
                },
                stop: function () {
                    return this.setZoom(this._limitZoom(this._zoom)), this.options.zoomSnap || this.fire("viewreset"), this._stop()
                },
                locate: function (t) {
                    if (t = this._locateOptions = i({
                        timeout: 1e4,
                        watch: !1
                    }, t), !("geolocation" in navigator)) return this._handleGeolocationError({
                        code: 0,
                        message: "Geolocation not supported."
                    }), this;
                    var e = n(this._handleGeolocationResponse, this), o = n(this._handleGeolocationError, this);
                    return t.watch ? this._locationWatchId = navigator.geolocation.watchPosition(e, o, t) : navigator.geolocation.getCurrentPosition(e, o, t), this
                },
                stopLocate: function () {
                    return navigator.geolocation && navigator.geolocation.clearWatch && navigator.geolocation.clearWatch(this._locationWatchId), this._locateOptions && (this._locateOptions.setView = !1), this
                },
                _handleGeolocationError: function (t) {
                    var i = t.code,
                        e = t.message || (1 === i ? "permission denied" : 2 === i ? "position unavailable" : "timeout");
                    this._locateOptions.setView && !this._loaded && this.fitWorld(), this.fire("locationerror", {
                        code: i,
                        message: "Geolocation error: " + e + "."
                    })
                },
                _handleGeolocationResponse: function (t) {
                    var i = new N(t.coords.latitude, t.coords.longitude), e = i.toBounds(2 * t.coords.accuracy),
                        n = this._locateOptions;
                    if (n.setView) {
                        var o = this.getBoundsZoom(e);
                        this.setView(i, n.maxZoom ? Math.min(o, n.maxZoom) : o)
                    }
                    var s = {latlng: i, bounds: e, timestamp: t.timestamp};
                    for (var r in t.coords) "number" == typeof t.coords[r] && (s[r] = t.coords[r]);
                    this.fire("locationfound", s)
                },
                addHandler: function (t, i) {
                    if (!i) return this;
                    var e = this[t] = new i(this);
                    return this._handlers.push(e), this.options[t] && e.enable(), this
                },
                remove: function () {
                    if (this._initEvents(!0), this.off("moveend", this._panInsideMaxBounds), this._containerId !== this._container._leaflet_id) throw new Error("Map container is being reused by another instance");
                    try {
                        delete this._container._leaflet_id, delete this._containerId
                    } catch (i) {
                        this._container._leaflet_id = void 0, this._containerId = void 0
                    }
                    var t;
                    for (t in void 0 !== this._locationWatchId && this.stopLocate(), this._stop(), ei(this._mapPane), this._clearControlPos && this._clearControlPos(), this._resizeRequest && (M(this._resizeRequest), this._resizeRequest = null), this._clearHandlers(), this._loaded && this.fire("unload"), this._layers) this._layers[t].remove();
                    for (t in this._panes) ei(this._panes[t]);
                    return this._layers = [], this._panes = [], delete this._mapPane, delete this._renderer, this
                },
                createPane: function (t, i) {
                    try {
                        var e = ii("div", "leaflet-pane" + (t ? " leaflet-" + t.replace("Pane", "") + "-pane" : ""), i || this._mapPane);
                    return t && (this._panes[t] = e), e
                    }catch (e) {

                    }

                },
                getCenter: function () {
                    return this._checkIfLoaded(), this._lastCenter && !this._moved() ? this._lastCenter : this.layerPointToLatLng(this._getCenterLayerPoint())
                },
                getZoom: function () {
                    return this._zoom
                },
                getBounds: function () {
                    var t = this.getPixelBounds();
                    return new O(this.unproject(t.getBottomLeft()), this.unproject(t.getTopRight()))
                },
                getMinZoom: function () {
                    return void 0 === this.options.minZoom ? this._layersMinZoom || 0 : this.options.minZoom
                },
                getMaxZoom: function () {
                    return void 0 === this.options.maxZoom ? void 0 === this._layersMaxZoom ? 1 / 0 : this._layersMaxZoom : this.options.maxZoom
                },
                getBoundsZoom: function (t, i, e) {
                    t = R(t), e = B(e || [0, 0]);
                    var n = this.getZoom() || 0, o = this.getMinZoom(), s = this.getMaxZoom(), r = t.getNorthWest(),
                        a = t.getSouthEast(), h = this.getSize().subtract(e),
                        u = I(this.project(a, n), this.project(r, n)).getSize(), l = mt ? this.options.zoomSnap : 1,
                        c = h.x / u.x, _ = h.y / u.y, d = i ? Math.max(c, _) : Math.min(c, _);
                    return n = this.getScaleZoom(d, n), l && (n = Math.round(n / (l / 100)) * (l / 100), n = i ? Math.ceil(n / l) * l : Math.floor(n / l) * l), Math.max(o, Math.min(s, n))
                },
                getSize: function () {
                    try {
                        return this._size && !this._sizeChanged || (this._size = new E(this._container.clientWidth || 0, this._container.clientHeight || 0), this._sizeChanged = !1), this._size.clone()
                    }catch (e) {
                        
                    }

                },
                getPixelBounds: function (t, i) {
                    var e = this._getTopLeftPoint(t, i);
                    return new A(e, e.add(this.getSize()))
                },
                getPixelOrigin: function () {
                    return this._checkIfLoaded(), this._pixelOrigin
                },
                getPixelWorldBounds: function (t) {
                    return this.options.crs.getProjectedBounds(void 0 === t ? this.getZoom() : t)
                },
                getPane: function (t) {
                    try {
                        return "string" == typeof t ? this._panes[t] : t
                    }catch (e) {

                    }

                },
                getPanes: function () {
                    return this._panes
                },
                getContainer: function () {
                    return this._container
                },
                getZoomScale: function (t, i) {
                    var e = this.options.crs;
                    return i = void 0 === i ? this._zoom : i, e.scale(t) / e.scale(i)
                },
                getScaleZoom: function (t, i) {
                    var e = this.options.crs;
                    i = void 0 === i ? this._zoom : i;
                    var n = e.zoom(t * e.scale(i));
                    return isNaN(n) ? 1 / 0 : n
                },
                project: function (t, i) {
                    return i = void 0 === i ? this._zoom : i, this.options.crs.latLngToPoint(D(t), i)
                },
                unproject: function (t, i) {
                    return i = void 0 === i ? this._zoom : i, this.options.crs.pointToLatLng(B(t), i)
                },
                layerPointToLatLng: function (t) {
                    var i = B(t).add(this.getPixelOrigin());
                    return this.unproject(i)
                },
                latLngToLayerPoint: function (t) {
                    return this.project(D(t))._round()._subtract(this.getPixelOrigin())
                },
                wrapLatLng: function (t) {
                    return this.options.crs.wrapLatLng(D(t))
                },
                wrapLatLngBounds: function (t) {
                    return this.options.crs.wrapLatLngBounds(R(t))
                },
                distance: function (t, i) {
                    return this.options.crs.distance(D(t), D(i))
                },
                containerPointToLayerPoint: function (t) {
                    return B(t).subtract(this._getMapPanePos())
                },
                layerPointToContainerPoint: function (t) {
                    return B(t).add(this._getMapPanePos())
                },
                containerPointToLatLng: function (t) {
                    var i = this.containerPointToLayerPoint(B(t));
                    return this.layerPointToLatLng(i)
                },
                latLngToContainerPoint: function (t) {
                    return this.layerPointToContainerPoint(this.latLngToLayerPoint(D(t)))
                },
                mouseEventToContainerPoint: function (t) {
                    return Oi(t, this._container)
                },
                mouseEventToLayerPoint: function (t) {
                    return this.containerPointToLayerPoint(this.mouseEventToContainerPoint(t))
                },
                mouseEventToLatLng: function (t) {
                    return this.layerPointToLatLng(this.mouseEventToLayerPoint(t))
                },
                _initContainer: function (t) {
                    try {
                        var i = this._container = Qt(t);
                        if (!i) throw new Error("Map container not found.");
                        if (i._leaflet_id) throw new Error("Map container is already initialized.");
                        bi(i, "scroll", this._onScroll, this), this._containerId = s(i)
                    } catch (e) {
                        
                    }

                },
                _initLayout: function () {
                    try {
                        var t = this._container;
                        this._fadeAnimated = this.options.fadeAnimation && mt, ai(t, "leaflet-container" + (wt ? " leaflet-touch" : "") + (bt ? " leaflet-retina" : "") + ($ ? " leaflet-oldie" : "") + (ht ? " leaflet-safari" : "") + (this._fadeAnimated ? " leaflet-fade-anim" : ""));
                        var i = ti(t, "position");
                        "absolute" !== i && "relative" !== i && "fixed" !== i && (t.style.position = "relative"), this._initPanes(), this._initControlPos && this._initControlPos()
                    } catch (e) {
                    }

                },
                _initPanes: function () {
                    var t = this._panes = {};
                    this._paneRenderers = {}, this._mapPane = this.createPane("mapPane", this._container), pi(this._mapPane, new E(0, 0)), this.createPane("tilePane"), this.createPane("shadowPane"), this.createPane("overlayPane"), this.createPane("markerPane"), this.createPane("tooltipPane"), this.createPane("popupPane"), this.options.markerZoomAnimation || (ai(t.markerPane, "leaflet-zoom-hide"), ai(t.shadowPane, "leaflet-zoom-hide"))
                },
                _resetView: function (t, i) {
                    pi(this._mapPane, new E(0, 0));
                    var e = !this._loaded;
                    this._loaded = !0, i = this._limitZoom(i), this.fire("viewprereset");
                    var n = this._zoom !== i;
                    this._moveStart(n, !1)._move(t, i)._moveEnd(n), this.fire("viewreset"), e && this.fire("load")
                },
                _moveStart: function (t, i) {
                    return t && this.fire("zoomstart"), i || this.fire("movestart"), this
                },
                _move: function (t, i, e) {
                    void 0 === i && (i = this._zoom);
                    var n = this._zoom !== i;
                    return this._zoom = i, this._lastCenter = t, this._pixelOrigin = this._getNewPixelOrigin(t), (n || e && e.pinch) && this.fire("zoom", e), this.fire("move", e)
                },
                _moveEnd: function (t) {
                    return t && this.fire("zoomend"), this.fire("moveend")
                },
                _stop: function () {
                    return M(this._flyToFrame), this._panAnim && this._panAnim.stop(), this
                },
                _rawPanBy: function (t) {
                    pi(this._mapPane, this._getMapPanePos().subtract(t))
                },
                _getZoomSpan: function () {
                    return this.getMaxZoom() - this.getMinZoom()
                },
                _panInsideMaxBounds: function () {
                    this._enforcingBounds || this.panInsideBounds(this.options.maxBounds)
                },
                _checkIfLoaded: function () {
                    if (!this._loaded) throw new Error("Set map center and zoom first.")
                },
                _initEvents: function (t) {
                    this._targets = {}, this._targets[s(this._container)] = this;
                    var i = t ? Mi : bi;
                    i(this._container, "click dblclick mousedown mouseup mouseover mouseout mousemove contextmenu keypress keydown keyup", this._handleDOMEvent, this), this.options.trackResize && i(window, "resize", this._onResize, this), mt && this.options.transform3DLimit && (t ? this.off : this.on).call(this, "moveend", this._onMoveEnd)
                },
                _onResize: function () {
                    M(this._resizeRequest), this._resizeRequest = T(function () {
                        this.invalidateSize({debounceMoveend: !0})
                    }, this)
                },
                _onScroll: function () {
                    this._container.scrollTop = 0, this._container.scrollLeft = 0
                },
                _onMoveEnd: function () {
                    var t = this._getMapPanePos();
                    Math.max(Math.abs(t.x), Math.abs(t.y)) >= this.options.transform3DLimit && this._resetView(this.getCenter(), this.getZoom())
                },
                _findEventTargets: function (t, i) {
                    for (var e, n = [], o = "mouseout" === i || "mouseover" === i, r = t.target || t.srcElement, a = !1; r;) {
                        if ((e = this._targets[s(r)]) && ("click" === i || "preclick" === i) && !t._simulated && this._draggableMoved(e)) {
                            a = !0;
                            break
                        }
                        if (e && e.listens(i, !0)) {
                            if (o && !Hi(r, t)) break;
                            if (n.push(e), o) break
                        }
                        if (r === this._container) break;
                        r = r.parentNode
                    }
                    return n.length || a || o || !Hi(r, t) || (n = [this]), n
                },
                _handleDOMEvent: function (t) {
                    if (this._loaded && !Wi(t)) {
                        var i = t.type;
                        "mousedown" !== i && "keypress" !== i && "keyup" !== i && "keydown" !== i || yi(t.target || t.srcElement), this._fireDOMEvent(t, i)
                    }
                },
                _mouseEvents: ["click", "dblclick", "mouseover", "mouseout", "contextmenu"],
                _fireDOMEvent: function (t, e, n) {
                    if ("click" === t.type) {
                        var o = i({}, t);
                        o.type = "preclick", this._fireDOMEvent(o, o.type, n)
                    }
                    if (!t._stopped && (n = (n || []).concat(this._findEventTargets(t, e))).length) {
                        var s = n[0];
                        "contextmenu" === e && s.listens(e, !0) && Ai(t);
                        var r = {originalEvent: t};
                        if ("keypress" !== t.type && "keydown" !== t.type && "keyup" !== t.type) {
                            var a = s.getLatLng && (!s._radius || s._radius <= 10);
                            r.containerPoint = a ? this.latLngToContainerPoint(s.getLatLng()) : this.mouseEventToContainerPoint(t), r.layerPoint = this.containerPointToLayerPoint(r.containerPoint), r.latlng = a ? s.getLatLng() : this.layerPointToLatLng(r.layerPoint)
                        }
                        for (var h = 0; h < n.length; h++) if (n[h].fire(e, r, !0), r.originalEvent._stopped || !1 === n[h].options.bubblingMouseEvents && -1 !== g(this._mouseEvents, e)) return
                    }
                },
                _draggableMoved: function (t) {
                    return (t = t.dragging && t.dragging.enabled() ? t : this).dragging && t.dragging.moved() || this.boxZoom && this.boxZoom.moved()
                },
                _clearHandlers: function () {
                    for (var t = 0, i = this._handlers.length; t < i; t++) this._handlers[t].disable()
                },
                whenReady: function (t, i) {
                    return this._loaded ? t.call(i || this, {target: this}) : this.on("load", t, i), this
                },
                _getMapPanePos: function () {
                    return mi(this._mapPane) || new E(0, 0)
                },
                _moved: function () {
                    var t = this._getMapPanePos();
                    return t && !t.equals([0, 0])
                },
                _getTopLeftPoint: function (t, i) {
                    return (t && void 0 !== i ? this._getNewPixelOrigin(t, i) : this.getPixelOrigin()).subtract(this._getMapPanePos())
                },
                _getNewPixelOrigin: function (t, i) {
                    try {
                        var e = this.getSize()._divideBy(2);
                    return this.project(t, i)._subtract(e)._add(this._getMapPanePos())._round()
                    }catch (e) {
                        
                    }

                },
                _latLngToNewLayerPoint: function (t, i, e) {
                    var n = this._getNewPixelOrigin(e, i);
                    return this.project(t, i)._subtract(n)
                },
                _latLngBoundsToNewLayerBounds: function (t, i, e) {
                    var n = this._getNewPixelOrigin(e, i);
                    return I([this.project(t.getSouthWest(), i)._subtract(n), this.project(t.getNorthWest(), i)._subtract(n), this.project(t.getSouthEast(), i)._subtract(n), this.project(t.getNorthEast(), i)._subtract(n)])
                },
                _getCenterLayerPoint: function () {
                    return this.containerPointToLayerPoint(this.getSize()._divideBy(2))
                },
                _getCenterOffset: function (t) {
                    return this.latLngToLayerPoint(t).subtract(this._getCenterLayerPoint())
                },
                _limitCenter: function (t, i, e) {
                    if (!e) return t;
                    var n = this.project(t, i), o = this.getSize().divideBy(2), s = new A(n.subtract(o), n.add(o)),
                        r = this._getBoundsOffset(s, e, i);
                    return r.round().equals([0, 0]) ? t : this.unproject(n.add(r), i)
                },
                _limitOffset: function (t, i) {
                    if (!i) return t;
                    var e = this.getPixelBounds(), n = new A(e.min.add(t), e.max.add(t));
                    return t.add(this._getBoundsOffset(n, i))
                },
                _getBoundsOffset: function (t, i, e) {
                    var n = I(this.project(i.getNorthEast(), e), this.project(i.getSouthWest(), e)),
                        o = n.min.subtract(t.min), s = n.max.subtract(t.max);
                    return new E(this._rebound(o.x, -s.x), this._rebound(o.y, -s.y))
                },
                _rebound: function (t, i) {
                    return t + i > 0 ? Math.round(t - i) / 2 : Math.max(0, Math.ceil(t)) - Math.max(0, Math.floor(i))
                },
                _limitZoom: function (t) {
                    var i = this.getMinZoom(), e = this.getMaxZoom(), n = mt ? this.options.zoomSnap : 1;
                    return n && (t = Math.round(t / n) * n), Math.max(i, Math.min(e, t))
                },
                _onPanTransitionStep: function () {
                    this.fire("move")
                },
                _onPanTransitionEnd: function () {
                    hi(this._mapPane, "leaflet-pan-anim"), this.fire("moveend")
                },
                _tryAnimatedPan: function (t, i) {
                    var e = this._getCenterOffset(t)._trunc();
                    return !(!0 !== (i && i.animate) && !this.getSize().contains(e)) && (this.panBy(e, i), !0)
                },
                _createAnimProxy: function () {
                    try {
                        var t = this._proxy = ii("div", "leaflet-proxy leaflet-zoom-animated");
                    this._panes.mapPane.appendChild(t), this.on("zoomanim", function (t) {
                        var i = Xt, e = this._proxy.style[i];
                        di(this._proxy, this.project(t.center, t.zoom), this.getZoomScale(t.zoom, 1)), e === this._proxy.style[i] && this._animatingZoom && this._onZoomTransitionEnd()
                    }, this), this.on("load moveend", this._animMoveEnd, this), this._on("unload", this._destroyAnimProxy, this)
                    }catch (e) {

                    }

                },
                _destroyAnimProxy: function () {
                    ei(this._proxy), this.off("load moveend", this._animMoveEnd, this), delete this._proxy
                },
                _animMoveEnd: function () {
                    var t = this.getCenter(), i = this.getZoom();
                    di(this._proxy, this.project(t, i), this.getZoomScale(i, 1))
                },
                _catchTransitionEnd: function (t) {
                    this._animatingZoom && t.propertyName.indexOf("transform") >= 0 && this._onZoomTransitionEnd()
                },
                _nothingToAnimate: function () {
                    return !this._container.getElementsByClassName("leaflet-zoom-animated").length
                },
                _tryAnimatedZoom: function (t, i, e) {
                    if (this._animatingZoom) return !0;
                    if (e = e || {}, !this._zoomAnimated || !1 === e.animate || this._nothingToAnimate() || Math.abs(i - this._zoom) > this.options.zoomAnimationThreshold) return !1;
                    var n = this.getZoomScale(i), o = this._getCenterOffset(t)._divideBy(1 - 1 / n);
                    return !(!0 !== e.animate && !this.getSize().contains(o)) && (T(function () {
                        this._moveStart(!0, !1)._animateZoom(t, i, !0)
                    }, this), !0)
                },
                _animateZoom: function (t, i, e, o) {
                    this._mapPane && (e && (this._animatingZoom = !0, this._animateToCenter = t, this._animateToZoom = i, ai(this._mapPane, "leaflet-zoom-anim")), this.fire("zoomanim", {
                        center: t,
                        zoom: i,
                        noUpdate: o
                    }), setTimeout(n(this._onZoomTransitionEnd, this), 250))
                },
                _onZoomTransitionEnd: function () {
                    this._animatingZoom && (this._mapPane && hi(this._mapPane, "leaflet-zoom-anim"), this._animatingZoom = !1, this._move(this._animateToCenter, this._animateToZoom), T(function () {
                        this._moveEnd(!0)
                    }, this))
                }
            });
            var qi = C.extend({
                options: {position: "topright"}, initialize: function (t) {
                    _(this, t)
                }, getPosition: function () {
                    return this.options.position
                }, setPosition: function (t) {
                    var i = this._map;
                    return i && i.removeControl(this), this.options.position = t, i && i.addControl(this), this
                }, getContainer: function () {
                    return this._container
                }, addTo: function (t) {
                    try {
                        this.remove(), this._map = t;
                    var i = this._container = this.onAdd(t), e = this.getPosition(), n = t._controlCorners[e];
                    return ai(i, "leaflet-control"), -1 !== e.indexOf("bottom") ? n.insertBefore(i, n.firstChild) : n.appendChild(i), this._map.on("unload", this.remove, this), this
                    }catch (e) {

                    }

                }, remove: function () {
                    return this._map ? (ei(this._container), this.onRemove && this.onRemove(this._map), this._map.off("unload", this.remove, this), this._map = null, this) : this
                }, _refocusOnMap: function (t) {
                    this._map && t && t.screenX > 0 && t.screenY > 0 && this._map.getContainer().focus()
                }
            }), Gi = function (t) {
                return new qi(t)
            };
            Vi.include({
                addControl: function (t) {
                    return t.addTo(this), this
                }, removeControl: function (t) {
                    return t.remove(), this
                }, _initControlPos: function () {
                    var t = this._controlCorners = {}, i = "leaflet-",
                        e = this._controlContainer = ii("div", i + "control-container", this._container);

                    function n(n, o) {
                        var s = i + n + " " + i + o;
                        t[n + o] = ii("div", s, e)
                    }

                    n("top", "left"), n("top", "right"), n("bottom", "left"), n("bottom", "right")
                }, _clearControlPos: function () {
                    for (var t in this._controlCorners) ei(this._controlCorners[t]);
                    ei(this._controlContainer), delete this._controlCorners, delete this._controlContainer
                }
            });
            var Ki = qi.extend({
                options: {
                    collapsed: !0,
                    position: "topright",
                    autoZIndex: !0,
                    hideSingleBase: !1,
                    sortLayers: !1,
                    sortFunction: function (t, i, e, n) {
                        return e < n ? -1 : n < e ? 1 : 0
                    }
                }, initialize: function (t, i, e) {
                    for (var n in _(this, e), this._layerControlInputs = [], this._layers = [], this._lastZIndex = 0, this._handlingClick = !1, t) this._addLayer(t[n], n);
                    for (n in i) this._addLayer(i[n], n, !0)
                }, onAdd: function (t) {
                    this._initLayout(), this._update(), this._map = t, t.on("zoomend", this._checkDisabledLayers, this);
                    for (var i = 0; i < this._layers.length; i++) this._layers[i].layer.on("add remove", this._onLayerChange, this);
                    return this._container
                }, addTo: function (t) {
                    return qi.prototype.addTo.call(this, t), this._expandIfNotCollapsed()
                }, onRemove: function () {
                    this._map.off("zoomend", this._checkDisabledLayers, this);
                    for (var t = 0; t < this._layers.length; t++) this._layers[t].layer.off("add remove", this._onLayerChange, this)
                }, addBaseLayer: function (t, i) {
                    return this._addLayer(t, i), this._map ? this._update() : this
                }, addOverlay: function (t, i) {
                    return this._addLayer(t, i, !0), this._map ? this._update() : this
                }, removeLayer: function (t) {
                    t.off("add remove", this._onLayerChange, this);
                    var i = this._getLayer(s(t));
                    return i && this._layers.splice(this._layers.indexOf(i), 1), this._map ? this._update() : this
                }, expand: function () {
                    ai(this._container, "leaflet-control-layers-expanded"), this._section.style.height = null;
                    var t = this._map.getSize().y - (this._container.offsetTop + 50);
                    return t < this._section.clientHeight ? (ai(this._section, "leaflet-control-layers-scrollbar"), this._section.style.height = t + "px") : hi(this._section, "leaflet-control-layers-scrollbar"), this._checkDisabledLayers(), this
                }, collapse: function () {
                    return hi(this._container, "leaflet-control-layers-expanded"), this
                }, _initLayout: function () {
                    var t = "leaflet-control-layers", i = this._container = ii("div", t), e = this.options.collapsed;
                    i.setAttribute("aria-haspopup", !0), Bi(i), ki(i);
                    var n = this._section = ii("section", t + "-list");
                    e && (this._map.on("click", this.collapse, this), it || bi(i, {
                        mouseenter: this.expand,
                        mouseleave: this.collapse
                    }, this));
                    var o = this._layersLink = ii("a", t + "-toggle", i);
                    o.href = "#", o.title = "Layers", wt ? (bi(o, "click", Ii), bi(o, "click", this.expand, this)) : bi(o, "focus", this.expand, this), e || this.expand(), this._baseLayersList = ii("div", t + "-base", n), this._separator = ii("div", t + "-separator", n), this._overlaysList = ii("div", t + "-overlays", n), i.appendChild(n)
                }, _getLayer: function (t) {
                    for (var i = 0; i < this._layers.length; i++) if (this._layers[i] && s(this._layers[i].layer) === t) return this._layers[i]
                }, _addLayer: function (t, i, e) {
                    this._map && t.on("add remove", this._onLayerChange, this), this._layers.push({
                        layer: t,
                        name: i,
                        overlay: e
                    }), this.options.sortLayers && this._layers.sort(n(function (t, i) {
                        return this.options.sortFunction(t.layer, i.layer, t.name, i.name)
                    }, this)), this.options.autoZIndex && t.setZIndex && (this._lastZIndex++, t.setZIndex(this._lastZIndex)), this._expandIfNotCollapsed()
                }, _update: function () {
                    if (!this._container) return this;
                    ni(this._baseLayersList), ni(this._overlaysList), this._layerControlInputs = [];
                    var t, i, e, n, o = 0;
                    for (e = 0; e < this._layers.length; e++) n = this._layers[e], this._addItem(n), i = i || n.overlay, t = t || !n.overlay, o += n.overlay ? 0 : 1;
                    return this.options.hideSingleBase && (t = t && o > 1, this._baseLayersList.style.display = t ? "" : "none"), this._separator.style.display = i && t ? "" : "none", this
                }, _onLayerChange: function (t) {
                    this._handlingClick || this._update();
                    var i = this._getLayer(s(t.target)),
                        e = i.overlay ? "add" === t.type ? "overlayadd" : "overlayremove" : "add" === t.type ? "baselayerchange" : null;
                    e && this._map.fire(e, i)
                }, _createRadioElement: function (t, i) {
                    var e = '<input type="radio" class="leaflet-control-layers-selector" name="' + t + '"' + (i ? ' checked="checked"' : "") + "/>",
                        n = document.createElement("div");
                    return n.innerHTML = e, n.firstChild
                }, _addItem: function (t) {
                    var i, e = document.createElement("label"), n = this._map.hasLayer(t.layer);
                    t.overlay ? ((i = document.createElement("input")).type = "checkbox", i.className = "leaflet-control-layers-selector", i.defaultChecked = n) : i = this._createRadioElement("leaflet-base-layers_" + s(this), n), this._layerControlInputs.push(i), i.layerId = s(t.layer), bi(i, "click", this._onInputClick, this);
                    var o = document.createElement("span");
                    o.innerHTML = " " + t.name;
                    var r = document.createElement("div");
                    return e.appendChild(r), r.appendChild(i), r.appendChild(o), (t.overlay ? this._overlaysList : this._baseLayersList).appendChild(e), this._checkDisabledLayers(), e
                }, _onInputClick: function () {
                    var t, i, e = this._layerControlInputs, n = [], o = [];
                    this._handlingClick = !0;
                    for (var s = e.length - 1; s >= 0; s--) t = e[s], i = this._getLayer(t.layerId).layer, t.checked ? n.push(i) : t.checked || o.push(i);
                    for (s = 0; s < o.length; s++) this._map.hasLayer(o[s]) && this._map.removeLayer(o[s]);
                    for (s = 0; s < n.length; s++) this._map.hasLayer(n[s]) || this._map.addLayer(n[s]);
                    this._handlingClick = !1, this._refocusOnMap()
                }, _checkDisabledLayers: function () {
                    for (var t, i, e = this._layerControlInputs, n = this._map.getZoom(), o = e.length - 1; o >= 0; o--) t = e[o], i = this._getLayer(t.layerId).layer, t.disabled = void 0 !== i.options.minZoom && n < i.options.minZoom || void 0 !== i.options.maxZoom && n > i.options.maxZoom
                }, _expandIfNotCollapsed: function () {
                    return this._map && !this.options.collapsed && this.expand(), this
                }, _expand: function () {
                    return this.expand()
                }, _collapse: function () {
                    return this.collapse()
                }
            }), Yi = qi.extend({
                options: {
                    position: "topleft",
                    zoomInText: "+",
                    zoomInTitle: "Zoom in",
                    zoomOutText: "&#x2212;",
                    zoomOutTitle: "Zoom out"
                }, onAdd: function (t) {
                    var i = "leaflet-control-zoom", e = ii("div", i + " leaflet-bar"), n = this.options;
                    return this._zoomInButton = this._createButton(n.zoomInText, n.zoomInTitle, i + "-in", e, this._zoomIn), this._zoomOutButton = this._createButton(n.zoomOutText, n.zoomOutTitle, i + "-out", e, this._zoomOut), this._updateDisabled(), t.on("zoomend zoomlevelschange", this._updateDisabled, this), e
                }, onRemove: function (t) {
                    t.off("zoomend zoomlevelschange", this._updateDisabled, this)
                }, disable: function () {
                    return this._disabled = !0, this._updateDisabled(), this
                }, enable: function () {
                    return this._disabled = !1, this._updateDisabled(), this
                }, _zoomIn: function (t) {
                    !this._disabled && this._map._zoom < this._map.getMaxZoom() && this._map.zoomIn(this._map.options.zoomDelta * (t.shiftKey ? 3 : 1))
                }, _zoomOut: function (t) {
                    !this._disabled && this._map._zoom > this._map.getMinZoom() && this._map.zoomOut(this._map.options.zoomDelta * (t.shiftKey ? 3 : 1))
                }, _createButton: function (t, i, e, n, o) {
                    var s = ii("a", e, n);
                    return s.innerHTML = t, s.href = "#", s.title = i, s.setAttribute("role", "button"), s.setAttribute("aria-label", i), Bi(s), bi(s, "click", Ii), bi(s, "click", o, this), bi(s, "click", this._refocusOnMap, this), s
                }, _updateDisabled: function () {
                    var t = this._map, i = "leaflet-disabled";
                    hi(this._zoomInButton, i), hi(this._zoomOutButton, i), (this._disabled || t._zoom === t.getMinZoom()) && ai(this._zoomOutButton, i), (this._disabled || t._zoom === t.getMaxZoom()) && ai(this._zoomInButton, i)
                }
            });
            Vi.mergeOptions({zoomControl: !0}), Vi.addInitHook(function () {
                this.options.zoomControl && (this.zoomControl = new Yi, this.addControl(this.zoomControl))
            });
            var Xi = qi.extend({
                options: {position: "bottomleft", maxWidth: 100, metric: !0, imperial: !0}, onAdd: function (t) {
                    var i = ii("div", "leaflet-control-scale"), e = this.options;
                    return this._addScales(e, "leaflet-control-scale-line", i), t.on(e.updateWhenIdle ? "moveend" : "move", this._update, this), t.whenReady(this._update, this), i
                }, onRemove: function (t) {
                    t.off(this.options.updateWhenIdle ? "moveend" : "move", this._update, this)
                }, _addScales: function (t, i, e) {
                    t.metric && (this._mScale = ii("div", i, e)), t.imperial && (this._iScale = ii("div", i, e))
                }, _update: function () {
                    var t = this._map, i = t.getSize().y / 2,
                        e = t.distance(t.containerPointToLatLng([0, i]), t.containerPointToLatLng([this.options.maxWidth, i]));
                    this._updateScales(e)
                }, _updateScales: function (t) {
                    this.options.metric && t && this._updateMetric(t), this.options.imperial && t && this._updateImperial(t)
                }, _updateMetric: function (t) {
                    var i = this._getRoundNum(t), e = i < 1e3 ? i + " m" : i / 1e3 + " km";
                    this._updateScale(this._mScale, e, i / t)
                }, _updateImperial: function (t) {
                    var i, e, n, o = 3.2808399 * t;
                    o > 5280 ? (i = o / 5280, e = this._getRoundNum(i), this._updateScale(this._iScale, e + " mi", e / i)) : (n = this._getRoundNum(o), this._updateScale(this._iScale, n + " ft", n / o))
                }, _updateScale: function (t, i, e) {
                    t.style.width = Math.round(this.options.maxWidth * e) + "px", t.innerHTML = i
                }, _getRoundNum: function (t) {
                    var i = Math.pow(10, (Math.floor(t) + "").length - 1), e = t / i;
                    return i * (e = e >= 10 ? 10 : e >= 5 ? 5 : e >= 3 ? 3 : e >= 2 ? 2 : 1)
                }
            }), Ji = qi.extend({
                options: {
                    position: "bottomright",
                    prefix: '<a href="https://leafletjs.com" title="A JS library for interactive maps">Leaflet</a>'
                }, initialize: function (t) {
                    _(this, t), this._attributions = {}
                }, onAdd: function (t) {
                    for (var i in t.attributionControl = this, this._container = ii("div", "leaflet-control-attribution"), Bi(this._container), t._layers) t._layers[i].getAttribution && this.addAttribution(t._layers[i].getAttribution());
                    return this._update(), this._container
                }, setPrefix: function (t) {
                    return this.options.prefix = t, this._update(), this
                }, addAttribution: function (t) {
                    return t ? (this._attributions[t] || (this._attributions[t] = 0), this._attributions[t]++, this._update(), this) : this
                }, removeAttribution: function (t) {
                    return t ? (this._attributions[t] && (this._attributions[t]--, this._update()), this) : this
                }, _update: function () {
                    if (this._map) {
                        var t = [];
                        for (var i in this._attributions) this._attributions[i] && t.push(i);
                        var e = [];
                        this.options.prefix && e.push(this.options.prefix), t.length && e.push(t.join(", ")), this._container.innerHTML = e.join(" | ")
                    }
                }
            });
            Vi.mergeOptions({attributionControl: !0}), Vi.addInitHook(function () {
                this.options.attributionControl && (new Ji).addTo(this)
            });
            qi.Layers = Ki, qi.Zoom = Yi, qi.Scale = Xi, qi.Attribution = Ji, Gi.layers = function (t, i, e) {
                return new Ki(t, i, e)
            }, Gi.zoom = function (t) {
                return new Yi(t)
            }, Gi.scale = function (t) {
                return new Xi(t)
            }, Gi.attribution = function (t) {
                return new Ji(t)
            };
            var $i = C.extend({
                initialize: function (t) {
                    this._map = t
                }, enable: function () {
                    return this._enabled ? this : (this._enabled = !0, this.addHooks(), this)
                }, disable: function () {
                    return this._enabled ? (this._enabled = !1, this.removeHooks(), this) : this
                }, enabled: function () {
                    return !!this._enabled
                }
            });
            $i.addTo = function (t, i) {
                return t.addHandler(i, this), this
            };
            var Qi, te = {Events: S}, ie = wt ? "touchstart mousedown" : "mousedown",
                ee = {mousedown: "mouseup", touchstart: "touchend", pointerdown: "touchend", MSPointerDown: "touchend"},
                ne = {
                    mousedown: "mousemove",
                    touchstart: "touchmove",
                    pointerdown: "touchmove",
                    MSPointerDown: "touchmove"
                }, oe = Z.extend({
                    options: {clickTolerance: 3}, initialize: function (t, i, e, n) {
                        _(this, n), this._element = t, this._dragStartTarget = i || t, this._preventOutline = e
                    }, enable: function () {
                        this._enabled || (bi(this._dragStartTarget, ie, this._onDown, this), this._enabled = !0)
                    }, disable: function () {
                        this._enabled && (oe._dragging === this && this.finishDrag(), Mi(this._dragStartTarget, ie, this._onDown, this), this._enabled = !1, this._moved = !1)
                    }, _onDown: function (t) {
                        if (!t._simulated && this._enabled && (this._moved = !1, !ri(this._element, "leaflet-zoom-anim") && !(oe._dragging || t.shiftKey || 1 !== t.which && 1 !== t.button && !t.touches || (oe._dragging = this, this._preventOutline && yi(this._element), gi(), Vt(), this._moving)))) {
                            this.fire("down");
                            var i = t.touches ? t.touches[0] : t, e = wi(this._element);
                            this._startPoint = new E(i.clientX, i.clientY), this._parentScale = Pi(e), bi(document, ne[t.type], this._onMove, this), bi(document, ee[t.type], this._onUp, this)
                        }
                    }, _onMove: function (t) {
                        if (!t._simulated && this._enabled) if (t.touches && t.touches.length > 1) this._moved = !0; else {
                            var i = t.touches && 1 === t.touches.length ? t.touches[0] : t,
                                e = new E(i.clientX, i.clientY)._subtract(this._startPoint);
                            (e.x || e.y) && (Math.abs(e.x) + Math.abs(e.y) < this.options.clickTolerance || (e.x /= this._parentScale.x, e.y /= this._parentScale.y, Ai(t), this._moved || (this.fire("dragstart"), this._moved = !0, this._startPos = mi(this._element).subtract(e), ai(document.body, "leaflet-dragging"), this._lastTarget = t.target || t.srcElement, window.SVGElementInstance && this._lastTarget instanceof window.SVGElementInstance && (this._lastTarget = this._lastTarget.correspondingUseElement), ai(this._lastTarget, "leaflet-drag-target")), this._newPos = this._startPos.add(e), this._moving = !0, M(this._animRequest), this._lastEvent = t, this._animRequest = T(this._updatePosition, this, !0)))
                        }
                    }, _updatePosition: function () {
                        var t = {originalEvent: this._lastEvent};
                        this.fire("predrag", t), pi(this._element, this._newPos), this.fire("drag", t)
                    }, _onUp: function (t) {
                        !t._simulated && this._enabled && this.finishDrag()
                    }, finishDrag: function () {
                        for (var t in hi(document.body, "leaflet-dragging"), this._lastTarget && (hi(this._lastTarget, "leaflet-drag-target"), this._lastTarget = null), ne) Mi(document, ne[t], this._onMove, this), Mi(document, ee[t], this._onUp, this);
                        vi(), qt(), this._moved && this._moving && (M(this._animRequest), this.fire("dragend", {distance: this._newPos.distanceTo(this._startPos)})), this._moving = !1, oe._dragging = !1
                    }
                });

            function se(t, i) {
                if (!i || !t.length) return t.slice();
                var e = i * i;
                return t = function (t, i) {
                    var e = t.length, n = new (typeof Uint8Array != void 0 + "" ? Uint8Array : Array)(e);
                    n[0] = n[e - 1] = 1, function t(i, e, n, o, s) {
                        var r, a, h, u = 0;
                        for (a = o + 1; a <= s - 1; a++) (h = le(i[a], i[o], i[s], !0)) > u && (r = a, u = h);
                        u > n && (e[r] = 1, t(i, e, n, o, r), t(i, e, n, r, s))
                    }(t, n, i, 0, e - 1);
                    var o, s = [];
                    for (o = 0; o < e; o++) n[o] && s.push(t[o]);
                    return s
                }(t = function (t, i) {
                    for (var e = [t[0]], n = 1, o = 0, s = t.length; n < s; n++) r = t[n], a = t[o], h = void 0, u = void 0, h = a.x - r.x, u = a.y - r.y, h * h + u * u > i && (e.push(t[n]), o = n);
                    var r, a, h, u;
                    o < s - 1 && e.push(t[s - 1]);
                    return e
                }(t, e), e)
            }

            function re(t, i, e) {
                return Math.sqrt(le(t, i, e, !0))
            }

            function ae(t, i, e, n, o) {
                var s, r, a, h = n ? Qi : ue(t, e), u = ue(i, e);
                for (Qi = u; ;) {
                    if (!(h | u)) return [t, i];
                    if (h & u) return !1;
                    a = ue(r = he(t, i, s = h || u, e, o), e), s === h ? (t = r, h = a) : (i = r, u = a)
                }
            }

            function he(t, i, e, n, o) {
                var s, r, a = i.x - t.x, h = i.y - t.y, u = n.min, l = n.max;
                return 8 & e ? (s = t.x + a * (l.y - t.y) / h, r = l.y) : 4 & e ? (s = t.x + a * (u.y - t.y) / h, r = u.y) : 2 & e ? (s = l.x, r = t.y + h * (l.x - t.x) / a) : 1 & e && (s = u.x, r = t.y + h * (u.x - t.x) / a), new E(s, r, o)
            }

            function ue(t, i) {
                var e = 0;
                return t.x < i.min.x ? e |= 1 : t.x > i.max.x && (e |= 2), t.y < i.min.y ? e |= 4 : t.y > i.max.y && (e |= 8), e
            }

            function le(t, i, e, n) {
                var o, s = i.x, r = i.y, a = e.x - s, h = e.y - r, u = a * a + h * h;
                return u > 0 && ((o = ((t.x - s) * a + (t.y - r) * h) / u) > 1 ? (s = e.x, r = e.y) : o > 0 && (s += a * o, r += h * o)), a = t.x - s, h = t.y - r, n ? a * a + h * h : new E(s, r)
            }

            function ce(t) {
                return !f(t[0]) || "object" != typeof t[0][0] && void 0 !== t[0][0]
            }

            function _e(t) {
                return console.warn("Deprecated use of _flat, please use L.LineUtil.isFlat instead."), ce(t)
            }

            var de = {
                simplify: se,
                pointToSegmentDistance: re,
                closestPointOnSegment: function (t, i, e) {
                    return le(t, i, e)
                },
                clipSegment: ae,
                _getEdgeIntersection: he,
                _getBitCode: ue,
                _sqClosestPointOnSegment: le,
                isFlat: ce,
                _flat: _e
            };

            function pe(t, i, e) {
                var n, o, s, r, a, h, u, l, c, _ = [1, 4, 2, 8];
                for (o = 0, u = t.length; o < u; o++) t[o]._code = ue(t[o], i);
                for (r = 0; r < 4; r++) {
                    for (l = _[r], n = [], o = 0, s = (u = t.length) - 1; o < u; s = o++) a = t[o], h = t[s], a._code & l ? h._code & l || ((c = he(h, a, l, i, e))._code = ue(c, i), n.push(c)) : (h._code & l && ((c = he(h, a, l, i, e))._code = ue(c, i), n.push(c)), n.push(a));
                    t = n
                }
                return t
            }

            var me = {clipPolygon: pe}, fe = {
                    project: function (t) {
                        return new E(t.lng, t.lat)
                    }, unproject: function (t) {
                        return new N(t.y, t.x)
                    }, bounds: new A([-180, -90], [180, 90])
                }, ge = {
                    R: 6378137,
                    R_MINOR: 6356752.314245179,
                    bounds: new A([-20037508.34279, -15496570.73972], [20037508.34279, 18764656.23138]),
                    project: function (t) {
                        var i = Math.PI / 180, e = this.R, n = t.lat * i, o = this.R_MINOR / e, s = Math.sqrt(1 - o * o),
                            r = s * Math.sin(n), a = Math.tan(Math.PI / 4 - n / 2) / Math.pow((1 - r) / (1 + r), s / 2);
                        return n = -e * Math.log(Math.max(a, 1e-10)), new E(t.lng * i * e, n)
                    },
                    unproject: function (t) {
                        for (var i, e = 180 / Math.PI, n = this.R, o = this.R_MINOR / n, s = Math.sqrt(1 - o * o), r = Math.exp(-t.y / n), a = Math.PI / 2 - 2 * Math.atan(r), h = 0, u = .1; h < 15 && Math.abs(u) > 1e-7; h++) i = s * Math.sin(a), i = Math.pow((1 - i) / (1 + i), s / 2), a += u = Math.PI / 2 - 2 * Math.atan(r * i) - a;
                        return new N(a * e, t.x * e / n)
                    }
                }, ve = {LonLat: fe, Mercator: ge, SphericalMercator: F}, ye = i({}, H, {
                    code: "EPSG:3395", projection: ge, transformation: function () {
                        var t = .5 / (Math.PI * ge.R);
                        return V(t, .5, -t, .5)
                    }()
                }), xe = i({}, H, {code: "EPSG:4326", projection: fe, transformation: V(1 / 180, 1, -1 / 180, .5)}),
                we = i({}, W, {
                    projection: fe, transformation: V(1, 0, -1, 0), scale: function (t) {
                        return Math.pow(2, t)
                    }, zoom: function (t) {
                        return Math.log(t) / Math.LN2
                    }, distance: function (t, i) {
                        var e = i.lng - t.lng, n = i.lat - t.lat;
                        return Math.sqrt(e * e + n * n)
                    }, infinite: !0
                });
            W.Earth = H, W.EPSG3395 = ye, W.EPSG3857 = q, W.EPSG900913 = G, W.EPSG4326 = xe, W.Simple = we;
            var Pe = Z.extend({
                options: {pane: "overlayPane", attribution: null, bubblingMouseEvents: !0},
                addTo: function (t) {
                    return t.addLayer(this), this
                },
                remove: function () {
                    return this.removeFrom(this._map || this._mapToAdd)
                },
                removeFrom: function (t) {
                    return t && t.removeLayer(this), this
                },
                getPane: function (t) {
                    return this._map.getPane(t ? this.options[t] || t : this.options.pane)
                },
                addInteractiveTarget: function (t) {
                    return this._map._targets[s(t)] = this, this
                },
                removeInteractiveTarget: function (t) {
                    return delete this._map._targets[s(t)], this
                },
                getAttribution: function () {
                    return this.options.attribution
                },
                _layerAdd: function (t) {
                    var i = t.target;
                    if (i.hasLayer(this)) {
                        if (this._map = i, this._zoomAnimated = i._zoomAnimated, this.getEvents) {
                            var e = this.getEvents();
                            i.on(e, this), this.once("remove", function () {
                                i.off(e, this)
                            }, this)
                        }
                        this.onAdd(i), this.getAttribution && i.attributionControl && i.attributionControl.addAttribution(this.getAttribution()), this.fire("add"), i.fire("layeradd", {layer: this})
                    }
                }
            });
            Vi.include({
                addLayer: function (t) {
                    if (!t._layerAdd) throw new Error("The provided object is not a Layer.");
                    var i = s(t);
                    return this._layers[i] ? this : (this._layers[i] = t, t._mapToAdd = this, t.beforeAdd && t.beforeAdd(this), this.whenReady(t._layerAdd, t), this)
                }, removeLayer: function (t) {
                    var i = s(t);
                    return this._layers[i] ? (this._loaded && t.onRemove(this), t.getAttribution && this.attributionControl && this.attributionControl.removeAttribution(t.getAttribution()), delete this._layers[i], this._loaded && (this.fire("layerremove", {layer: t}), t.fire("remove")), t._map = t._mapToAdd = null, this) : this
                }, hasLayer: function (t) {
                    return !!t && s(t) in this._layers
                }, eachLayer: function (t, i) {
                    for (var e in this._layers) t.call(i, this._layers[e]);
                    return this
                }, _addLayers: function (t) {
                    for (var i = 0, e = (t = t ? f(t) ? t : [t] : []).length; i < e; i++) this.addLayer(t[i])
                }, _addZoomLimit: function (t) {
                    !isNaN(t.options.maxZoom) && isNaN(t.options.minZoom) || (this._zoomBoundLayers[s(t)] = t, this._updateZoomLevels())
                }, _removeZoomLimit: function (t) {
                    var i = s(t);
                    this._zoomBoundLayers[i] && (delete this._zoomBoundLayers[i], this._updateZoomLevels())
                }, _updateZoomLevels: function () {
                    var t = 1 / 0, i = -1 / 0, e = this._getZoomSpan();
                    for (var n in this._zoomBoundLayers) {
                        var o = this._zoomBoundLayers[n].options;
                        t = void 0 === o.minZoom ? t : Math.min(t, o.minZoom), i = void 0 === o.maxZoom ? i : Math.max(i, o.maxZoom)
                    }
                    this._layersMaxZoom = i === -1 / 0 ? void 0 : i, this._layersMinZoom = t === 1 / 0 ? void 0 : t, e !== this._getZoomSpan() && this.fire("zoomlevelschange"), void 0 === this.options.maxZoom && this._layersMaxZoom && this.getZoom() > this._layersMaxZoom && this.setZoom(this._layersMaxZoom), void 0 === this.options.minZoom && this._layersMinZoom && this.getZoom() < this._layersMinZoom && this.setZoom(this._layersMinZoom)
                }
            });
            var Le = Pe.extend({
                initialize: function (t, i) {
                    var e, n;
                    if (_(this, i), this._layers = {}, t) for (e = 0, n = t.length; e < n; e++) this.addLayer(t[e])
                }, addLayer: function (t) {
                    var i = this.getLayerId(t);
                    return this._layers[i] = t, this._map && this._map.addLayer(t), this
                }, removeLayer: function (t) {
                    var i = t in this._layers ? t : this.getLayerId(t);
                    return this._map && this._layers[i] && this._map.removeLayer(this._layers[i]), delete this._layers[i], this
                }, hasLayer: function (t) {
                    return !!t && ("number" == typeof t ? t : this.getLayerId(t)) in this._layers
                }, clearLayers: function () {
                    return this.eachLayer(this.removeLayer, this)
                }, invoke: function (t) {
                    var i, e, n = Array.prototype.slice.call(arguments, 1);
                    for (i in this._layers) (e = this._layers[i])[t] && e[t].apply(e, n);
                    return this
                }, onAdd: function (t) {
                    this.eachLayer(t.addLayer, t)
                }, onRemove: function (t) {
                    this.eachLayer(t.removeLayer, t)
                }, eachLayer: function (t, i) {
                    for (var e in this._layers) t.call(i, this._layers[e]);
                    return this
                }, getLayer: function (t) {
                    return this._layers[t]
                }, getLayers: function () {
                    var t = [];
                    return this.eachLayer(t.push, t), t
                }, setZIndex: function (t) {
                    return this.invoke("setZIndex", t)
                }, getLayerId: function (t) {
                    return s(t)
                }
            }), be = Le.extend({
                addLayer: function (t) {
                    return this.hasLayer(t) ? this : (t.addEventParent(this), Le.prototype.addLayer.call(this, t), this.fire("layeradd", {layer: t}))
                }, removeLayer: function (t) {
                    return this.hasLayer(t) ? (t in this._layers && (t = this._layers[t]), t.removeEventParent(this), Le.prototype.removeLayer.call(this, t), this.fire("layerremove", {layer: t})) : this
                }, setStyle: function (t) {
                    return this.invoke("setStyle", t)
                }, bringToFront: function () {
                    return this.invoke("bringToFront")
                }, bringToBack: function () {
                    return this.invoke("bringToBack")
                }, getBounds: function () {
                    var t = new O;
                    for (var i in this._layers) {
                        var e = this._layers[i];
                        t.extend(e.getBounds ? e.getBounds() : e.getLatLng())
                    }
                    return t
                }
            }), Te = C.extend({
                options: {popupAnchor: [0, 0], tooltipAnchor: [0, 0]}, initialize: function (t) {
                    _(this, t)
                }, createIcon: function (t) {
                    return this._createIcon("icon", t)
                }, createShadow: function (t) {
                    return this._createIcon("shadow", t)
                }, _createIcon: function (t, i) {
                    var e = this._getIconUrl(t);
                    if (!e) {
                        if ("icon" === t) throw new Error("iconUrl not set in Icon options (see the docs).");
                        return null
                    }
                    var n = this._createImg(e, i && "IMG" === i.tagName ? i : null);
                    return this._setIconStyles(n, t), n
                }, _setIconStyles: function (t, i) {
                    var e = this.options, n = e[i + "Size"];
                    "number" == typeof n && (n = [n, n]);
                    var o = B(n), s = B("shadow" === i && e.shadowAnchor || e.iconAnchor || o && o.divideBy(2, !0));
                    t.className = "leaflet-marker-" + i + " " + (e.className || ""), s && (t.style.marginLeft = -s.x + "px", t.style.marginTop = -s.y + "px"), o && (t.style.width = o.x + "px", t.style.height = o.y + "px")
                }, _createImg: function (t, i) {
                    return (i = i || document.createElement("img")).src = t, i
                }, _getIconUrl: function (t) {
                    return bt && this.options[t + "RetinaUrl"] || this.options[t + "Url"]
                }
            });
            var Me = Te.extend({
                options: {
                    iconUrl: "marker-icon.png",
                    iconRetinaUrl: "marker-icon-2x.png",
                    shadowUrl: "marker-shadow.png",
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    tooltipAnchor: [16, -28],
                    shadowSize: [41, 41]
                }, _getIconUrl: function (t) {
                    return Me.imagePath || (Me.imagePath = this._detectIconPath()), (this.options.imagePath || Me.imagePath) + Te.prototype._getIconUrl.call(this, t)
                }, _detectIconPath: function () {
                    var t = ii("div", "leaflet-default-icon-path", document.body),
                        i = ti(t, "background-image") || ti(t, "backgroundImage");
                    return document.body.removeChild(t), i = null === i || 0 !== i.indexOf("url") ? "" : i.replace(/^url\(["']?/, "").replace(/marker-icon\.png["']?\)$/, "")
                }
            }), ze = $i.extend({
                initialize: function (t) {
                    this._marker = t
                }, addHooks: function () {
                    var t = this._marker._icon;
                    this._draggable || (this._draggable = new oe(t, t, !0)), this._draggable.on({
                        dragstart: this._onDragStart,
                        predrag: this._onPreDrag,
                        drag: this._onDrag,
                        dragend: this._onDragEnd
                    }, this).enable(), ai(t, "leaflet-marker-draggable")
                }, removeHooks: function () {
                    this._draggable.off({
                        dragstart: this._onDragStart,
                        predrag: this._onPreDrag,
                        drag: this._onDrag,
                        dragend: this._onDragEnd
                    }, this).disable(), this._marker._icon && hi(this._marker._icon, "leaflet-marker-draggable")
                }, moved: function () {
                    return this._draggable && this._draggable._moved
                }, _adjustPan: function (t) {
                    var i = this._marker, e = i._map, n = this._marker.options.autoPanSpeed,
                        o = this._marker.options.autoPanPadding, s = mi(i._icon), r = e.getPixelBounds(),
                        a = e.getPixelOrigin(), h = I(r.min._subtract(a).add(o), r.max._subtract(a).subtract(o));
                    if (!h.contains(s)) {
                        var u = B((Math.max(h.max.x, s.x) - h.max.x) / (r.max.x - h.max.x) - (Math.min(h.min.x, s.x) - h.min.x) / (r.min.x - h.min.x), (Math.max(h.max.y, s.y) - h.max.y) / (r.max.y - h.max.y) - (Math.min(h.min.y, s.y) - h.min.y) / (r.min.y - h.min.y)).multiplyBy(n);
                        e.panBy(u, {animate: !1}), this._draggable._newPos._add(u), this._draggable._startPos._add(u), pi(i._icon, this._draggable._newPos), this._onDrag(t), this._panRequest = T(this._adjustPan.bind(this, t))
                    }
                }, _onDragStart: function () {
                    this._oldLatLng = this._marker.getLatLng(), this._marker.closePopup && this._marker.closePopup(), this._marker.fire("movestart").fire("dragstart")
                }, _onPreDrag: function (t) {
                    this._marker.options.autoPan && (M(this._panRequest), this._panRequest = T(this._adjustPan.bind(this, t)))
                }, _onDrag: function (t) {
                    var i = this._marker, e = i._shadow, n = mi(i._icon), o = i._map.layerPointToLatLng(n);
                    e && pi(e, n), i._latlng = o, t.latlng = o, t.oldLatLng = this._oldLatLng, i.fire("move", t).fire("drag", t)
                }, _onDragEnd: function (t) {
                    M(this._panRequest), delete this._oldLatLng, this._marker.fire("moveend").fire("dragend", t)
                }
            }), Ce = Pe.extend({
                options: {
                    icon: new Me,
                    interactive: !0,
                    keyboard: !0,
                    title: "",
                    alt: "",
                    zIndexOffset: 0,
                    opacity: 1,
                    riseOnHover: !1,
                    riseOffset: 250,
                    pane: "markerPane",
                    shadowPane: "shadowPane",
                    bubblingMouseEvents: !1,
                    draggable: !1,
                    autoPan: !1,
                    autoPanPadding: [50, 50],
                    autoPanSpeed: 10
                }, initialize: function (t, i) {
                    _(this, i), this._latlng = D(t)
                }, onAdd: function (t) {
                    this._zoomAnimated = this._zoomAnimated && t.options.markerZoomAnimation, this._zoomAnimated && t.on("zoomanim", this._animateZoom, this), this._initIcon(), this.update()
                }, onRemove: function (t) {
                    this.dragging && this.dragging.enabled() && (this.options.draggable = !0, this.dragging.removeHooks()), delete this.dragging, this._zoomAnimated && t.off("zoomanim", this._animateZoom, this), this._removeIcon(), this._removeShadow()
                }, getEvents: function () {
                    return {zoom: this.update, viewreset: this.update}
                }, getLatLng: function () {
                    return this._latlng
                }, setLatLng: function (t) {
                    var i = this._latlng;
                    return this._latlng = D(t), this.update(), this.fire("move", {oldLatLng: i, latlng: this._latlng})
                }, setZIndexOffset: function (t) {
                    return this.options.zIndexOffset = t, this.update()
                }, getIcon: function () {
                    return this.options.icon
                }, setIcon: function (t) {
                    return this.options.icon = t, this._map && (this._initIcon(), this.update()), this._popup && this.bindPopup(this._popup, this._popup.options), this
                }, getElement: function () {
                    return this._icon
                }, update: function () {
                    if (this._icon && this._map) {
                        var t = this._map.latLngToLayerPoint(this._latlng).round();
                        this._setPos(t)
                    }
                    return this
                }, _initIcon: function () {
                    var t = this.options, i = "leaflet-zoom-" + (this._zoomAnimated ? "animated" : "hide"),
                        e = t.icon.createIcon(this._icon), n = !1;
                    e !== this._icon && (this._icon && this._removeIcon(), n = !0, t.title && (e.title = t.title), "IMG" === e.tagName && (e.alt = t.alt || "")), ai(e, i), t.keyboard && (e.tabIndex = "0"), this._icon = e, t.riseOnHover && this.on({
                        mouseover: this._bringToFront,
                        mouseout: this._resetZIndex
                    });
                    var o = t.icon.createShadow(this._shadow), s = !1;
                    o !== this._shadow && (this._removeShadow(), s = !0), o && (ai(o, i), o.alt = ""), this._shadow = o, t.opacity < 1 && this._updateOpacity(), n && this.getPane().appendChild(this._icon), this._initInteraction(), o && s && this.getPane(t.shadowPane).appendChild(this._shadow)
                }, _removeIcon: function () {
                    this.options.riseOnHover && this.off({
                        mouseover: this._bringToFront,
                        mouseout: this._resetZIndex
                    }), ei(this._icon), this.removeInteractiveTarget(this._icon), this._icon = null
                }, _removeShadow: function () {
                    this._shadow && ei(this._shadow), this._shadow = null
                }, _setPos: function (t) {
                    this._icon && pi(this._icon, t), this._shadow && pi(this._shadow, t), this._zIndex = t.y + this.options.zIndexOffset, this._resetZIndex()
                }, _updateZIndex: function (t) {
                    this._icon && (this._icon.style.zIndex = this._zIndex + t)
                }, _animateZoom: function (t) {
                    var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center).round();
                    this._setPos(i)
                }, _initInteraction: function () {
                    if (this.options.interactive && (ai(this._icon, "leaflet-interactive"), this.addInteractiveTarget(this._icon), ze)) {
                        var t = this.options.draggable;
                        this.dragging && (t = this.dragging.enabled(), this.dragging.disable()), this.dragging = new ze(this), t && this.dragging.enable()
                    }
                }, setOpacity: function (t) {
                    return this.options.opacity = t, this._map && this._updateOpacity(), this
                }, _updateOpacity: function () {
                    var t = this.options.opacity;
                    this._icon && ci(this._icon, t), this._shadow && ci(this._shadow, t)
                }, _bringToFront: function () {
                    this._updateZIndex(this.options.riseOffset)
                }, _resetZIndex: function () {
                    this._updateZIndex(0)
                }, _getPopupAnchor: function () {
                    return this.options.icon.options.popupAnchor
                }, _getTooltipAnchor: function () {
                    return this.options.icon.options.tooltipAnchor
                }
            });
            var Se = Pe.extend({
                options: {
                    stroke: !0,
                    color: "#3388ff",
                    weight: 3,
                    opacity: 1,
                    lineCap: "round",
                    lineJoin: "round",
                    dashArray: null,
                    dashOffset: null,
                    fill: !1,
                    fillColor: null,
                    fillOpacity: .2,
                    fillRule: "evenodd",
                    interactive: !0,
                    bubblingMouseEvents: !0
                }, beforeAdd: function (t) {
                    this._renderer = t.getRenderer(this)
                }, onAdd: function () {
                    this._renderer._initPath(this), this._reset(), this._renderer._addPath(this)
                }, onRemove: function () {
                    this._renderer._removePath(this)
                }, redraw: function () {
                    return this._map && this._renderer._updatePath(this), this
                }, setStyle: function (t) {
                    return _(this, t), this._renderer && (this._renderer._updateStyle(this), this.options.stroke && t && Object.prototype.hasOwnProperty.call(t, "weight") && this._updateBounds()), this
                }, bringToFront: function () {
                    return this._renderer && this._renderer._bringToFront(this), this
                }, bringToBack: function () {
                    return this._renderer && this._renderer._bringToBack(this), this
                }, getElement: function () {
                    return this._path
                }, _reset: function () {
                    this._project(), this._update()
                }, _clickTolerance: function () {
                    return (this.options.stroke ? this.options.weight / 2 : 0) + this._renderer.options.tolerance
                }
            }), Ze = Se.extend({
                options: {fill: !0, radius: 10}, initialize: function (t, i) {
                    _(this, i), this._latlng = D(t), this._radius = this.options.radius
                }, setLatLng: function (t) {
                    var i = this._latlng;
                    return this._latlng = D(t), this.redraw(), this.fire("move", {oldLatLng: i, latlng: this._latlng})
                }, getLatLng: function () {
                    return this._latlng
                }, setRadius: function (t) {
                    return this.options.radius = this._radius = t, this.redraw()
                }, getRadius: function () {
                    return this._radius
                }, setStyle: function (t) {
                    var i = t && t.radius || this._radius;
                    return Se.prototype.setStyle.call(this, t), this.setRadius(i), this
                }, _project: function () {
                    this._point = this._map.latLngToLayerPoint(this._latlng), this._updateBounds()
                }, _updateBounds: function () {
                    var t = this._radius, i = this._radiusY || t, e = this._clickTolerance(), n = [t + e, i + e];
                    this._pxBounds = new A(this._point.subtract(n), this._point.add(n))
                }, _update: function () {
                    this._map && this._updatePath()
                }, _updatePath: function () {
                    this._renderer._updateCircle(this)
                }, _empty: function () {
                    return this._radius && !this._renderer._bounds.intersects(this._pxBounds)
                }, _containsPoint: function (t) {
                    return t.distanceTo(this._point) <= this._radius + this._clickTolerance()
                }
            });
            var Ee = Ze.extend({
                initialize: function (t, e, n) {
                    if ("number" == typeof e && (e = i({}, n, {radius: e})), _(this, e), this._latlng = D(t), isNaN(this.options.radius)) throw new Error("Circle radius cannot be NaN");
                    this._mRadius = this.options.radius
                }, setRadius: function (t) {
                    return this._mRadius = t, this.redraw()
                }, getRadius: function () {
                    return this._mRadius
                }, getBounds: function () {
                    var t = [this._radius, this._radiusY || this._radius];
                    return new O(this._map.layerPointToLatLng(this._point.subtract(t)), this._map.layerPointToLatLng(this._point.add(t)))
                }, setStyle: Se.prototype.setStyle, _project: function () {
                    var t = this._latlng.lng, i = this._latlng.lat, e = this._map, n = e.options.crs;
                    if (n.distance === H.distance) {
                        var o = Math.PI / 180, s = this._mRadius / H.R / o, r = e.project([i + s, t]),
                            a = e.project([i - s, t]), h = r.add(a).divideBy(2), u = e.unproject(h).lat,
                            l = Math.acos((Math.cos(s * o) - Math.sin(i * o) * Math.sin(u * o)) / (Math.cos(i * o) * Math.cos(u * o))) / o;
                        (isNaN(l) || 0 === l) && (l = s / Math.cos(Math.PI / 180 * i)), this._point = h.subtract(e.getPixelOrigin()), this._radius = isNaN(l) ? 0 : h.x - e.project([u, t - l]).x, this._radiusY = h.y - r.y
                    } else {
                        var c = n.unproject(n.project(this._latlng).subtract([this._mRadius, 0]));
                        this._point = e.latLngToLayerPoint(this._latlng), this._radius = this._point.x - e.latLngToLayerPoint(c).x
                    }
                    this._updateBounds()
                }
            });
            var ke = Se.extend({
                options: {smoothFactor: 1, noClip: !1}, initialize: function (t, i) {
                    _(this, i), this._setLatLngs(t)
                }, getLatLngs: function () {
                    return this._latlngs
                }, setLatLngs: function (t) {
                    return this._setLatLngs(t), this.redraw()
                }, isEmpty: function () {
                    return !this._latlngs.length
                }, closestLayerPoint: function (t) {
                    for (var i, e, n = 1 / 0, o = null, s = le, r = 0, a = this._parts.length; r < a; r++) for (var h = this._parts[r], u = 1, l = h.length; u < l; u++) {
                        var c = s(t, i = h[u - 1], e = h[u], !0);
                        c < n && (n = c, o = s(t, i, e))
                    }
                    return o && (o.distance = Math.sqrt(n)), o
                }, getCenter: function () {
                    if (!this._map) throw new Error("Must add layer to map before using getCenter()");
                    var t, i, e, n, o, s, r, a = this._rings[0], h = a.length;
                    if (!h) return null;
                    for (t = 0, i = 0; t < h - 1; t++) i += a[t].distanceTo(a[t + 1]) / 2;
                    if (0 === i) return this._map.layerPointToLatLng(a[0]);
                    for (t = 0, n = 0; t < h - 1; t++) if (o = a[t], s = a[t + 1], (n += e = o.distanceTo(s)) > i) return r = (n - i) / e, this._map.layerPointToLatLng([s.x - r * (s.x - o.x), s.y - r * (s.y - o.y)])
                }, getBounds: function () {
                    return this._bounds
                }, addLatLng: function (t, i) {
                    return i = i || this._defaultShape(), t = D(t), i.push(t), this._bounds.extend(t), this.redraw()
                }, _setLatLngs: function (t) {
                    this._bounds = new O, this._latlngs = this._convertLatLngs(t)
                }, _defaultShape: function () {
                    return ce(this._latlngs) ? this._latlngs : this._latlngs[0]
                }, _convertLatLngs: function (t) {
                    for (var i = [], e = ce(t), n = 0, o = t.length; n < o; n++) e ? (i[n] = D(t[n]), this._bounds.extend(i[n])) : i[n] = this._convertLatLngs(t[n]);
                    return i
                }, _project: function () {
                    var t = new A;
                    this._rings = [], this._projectLatlngs(this._latlngs, this._rings, t), this._bounds.isValid() && t.isValid() && (this._rawPxBounds = t, this._updateBounds())
                }, _updateBounds: function () {
                    var t = this._clickTolerance(), i = new E(t, t);
                    this._pxBounds = new A([this._rawPxBounds.min.subtract(i), this._rawPxBounds.max.add(i)])
                }, _projectLatlngs: function (t, i, e) {
                    var n, o, s = t[0] instanceof N, r = t.length;
                    if (s) {
                        for (o = [], n = 0; n < r; n++) o[n] = this._map.latLngToLayerPoint(t[n]), e.extend(o[n]);
                        i.push(o)
                    } else for (n = 0; n < r; n++) this._projectLatlngs(t[n], i, e)
                }, _clipPoints: function () {
                    var t = this._renderer._bounds;
                    if (this._parts = [], this._pxBounds && this._pxBounds.intersects(t)) if (this.options.noClip) this._parts = this._rings; else {
                        var i, e, n, o, s, r, a, h = this._parts;
                        for (i = 0, n = 0, o = this._rings.length; i < o; i++) for (e = 0, s = (a = this._rings[i]).length; e < s - 1; e++) (r = ae(a[e], a[e + 1], t, e, !0)) && (h[n] = h[n] || [], h[n].push(r[0]), r[1] === a[e + 1] && e !== s - 2 || (h[n].push(r[1]), n++))
                    }
                }, _simplifyPoints: function () {
                    for (var t = this._parts, i = this.options.smoothFactor, e = 0, n = t.length; e < n; e++) t[e] = se(t[e], i)
                }, _update: function () {
                    this._map && (this._clipPoints(), this._simplifyPoints(), this._updatePath())
                }, _updatePath: function () {
                    this._renderer._updatePoly(this)
                }, _containsPoint: function (t, i) {
                    var e, n, o, s, r, a, h = this._clickTolerance();
                    if (!this._pxBounds || !this._pxBounds.contains(t)) return !1;
                    for (e = 0, s = this._parts.length; e < s; e++) for (n = 0, o = (r = (a = this._parts[e]).length) - 1; n < r; o = n++) if ((i || 0 !== n) && re(t, a[o], a[n]) <= h) return !0;
                    return !1
                }
            });
            ke._flat = _e;
            var Be = ke.extend({
                options: {fill: !0}, isEmpty: function () {
                    return !this._latlngs.length || !this._latlngs[0].length
                }, getCenter: function () {
                    if (!this._map) throw new Error("Must add layer to map before using getCenter()");
                    var t, i, e, n, o, s, r, a, h, u = this._rings[0], l = u.length;
                    if (!l) return null;
                    for (s = r = a = 0, t = 0, i = l - 1; t < l; i = t++) e = u[t], n = u[i], o = e.y * n.x - n.y * e.x, r += (e.x + n.x) * o, a += (e.y + n.y) * o, s += 3 * o;
                    return h = 0 === s ? u[0] : [r / s, a / s], this._map.layerPointToLatLng(h)
                }, _convertLatLngs: function (t) {
                    var i = ke.prototype._convertLatLngs.call(this, t), e = i.length;
                    return e >= 2 && i[0] instanceof N && i[0].equals(i[e - 1]) && i.pop(), i
                }, _setLatLngs: function (t) {
                    ke.prototype._setLatLngs.call(this, t), ce(this._latlngs) && (this._latlngs = [this._latlngs])
                }, _defaultShape: function () {
                    return ce(this._latlngs[0]) ? this._latlngs[0] : this._latlngs[0][0]
                }, _clipPoints: function () {
                    var t = this._renderer._bounds, i = this.options.weight, e = new E(i, i);
                    if (t = new A(t.min.subtract(e), t.max.add(e)), this._parts = [], this._pxBounds && this._pxBounds.intersects(t)) if (this.options.noClip) this._parts = this._rings; else for (var n, o = 0, s = this._rings.length; o < s; o++) (n = pe(this._rings[o], t, !0)).length && this._parts.push(n)
                }, _updatePath: function () {
                    this._renderer._updatePoly(this, !0)
                }, _containsPoint: function (t) {
                    var i, e, n, o, s, r, a, h, u = !1;
                    if (!this._pxBounds || !this._pxBounds.contains(t)) return !1;
                    for (o = 0, a = this._parts.length; o < a; o++) for (s = 0, r = (h = (i = this._parts[o]).length) - 1; s < h; r = s++) e = i[s], n = i[r], e.y > t.y != n.y > t.y && t.x < (n.x - e.x) * (t.y - e.y) / (n.y - e.y) + e.x && (u = !u);
                    return u || ke.prototype._containsPoint.call(this, t, !0)
                }
            });
            var Ae = be.extend({
                initialize: function (t, i) {
                    _(this, i), this._layers = {}, t && this.addData(t)
                }, addData: function (t) {
                    var i, e, n, o = f(t) ? t : t.features;
                    if (o) {
                        for (i = 0, e = o.length; i < e; i++) ((n = o[i]).geometries || n.geometry || n.features || n.coordinates) && this.addData(n);
                        return this
                    }
                    var s = this.options;
                    if (s.filter && !s.filter(t)) return this;
                    var r = Ie(t, s);
                    return r ? (r.feature = He(t), r.defaultOptions = r.options, this.resetStyle(r), s.onEachFeature && s.onEachFeature(t, r), this.addLayer(r)) : this
                }, resetStyle: function (t) {
                    return void 0 === t ? this.eachLayer(this.resetStyle, this) : (t.options = i({}, t.defaultOptions), this._setLayerStyle(t, this.options.style), this)
                }, setStyle: function (t) {
                    return this.eachLayer(function (i) {
                        this._setLayerStyle(i, t)
                    }, this)
                }, _setLayerStyle: function (t, i) {
                    t.setStyle && ("function" == typeof i && (i = i(t.feature)), t.setStyle(i))
                }
            });

            function Ie(t, i) {
                var e, n, o, s, r = "Feature" === t.type ? t.geometry : t, a = r ? r.coordinates : null, h = [],
                    u = i && i.pointToLayer, l = i && i.coordsToLatLng || Re;
                if (!a && !r) return null;
                switch (r.type) {
                    case"Point":
                        return Oe(u, t, e = l(a), i);
                    case"MultiPoint":
                        for (o = 0, s = a.length; o < s; o++) e = l(a[o]), h.push(Oe(u, t, e, i));
                        return new be(h);
                    case"LineString":
                    case"MultiLineString":
                        return n = Ne(a, "LineString" === r.type ? 0 : 1, l), new ke(n, i);
                    case"Polygon":
                    case"MultiPolygon":
                        return n = Ne(a, "Polygon" === r.type ? 1 : 2, l), new Be(n, i);
                    case"GeometryCollection":
                        for (o = 0, s = r.geometries.length; o < s; o++) {
                            var c = Ie({geometry: r.geometries[o], type: "Feature", properties: t.properties}, i);
                            c && h.push(c)
                        }
                        return new be(h);
                    default:
                        throw new Error("Invalid GeoJSON object.")
                }
            }

            function Oe(t, i, e, n) {
                return t ? t(i, e) : new Ce(e, n && n.markersInheritOptions && n)
            }

            function Re(t) {
                return new N(t[1], t[0], t[2])
            }

            function Ne(t, i, e) {
                for (var n, o = [], s = 0, r = t.length; s < r; s++) n = i ? Ne(t[s], i - 1, e) : (e || Re)(t[s]), o.push(n);
                return o
            }

            function De(t, i) {
                return i = "number" == typeof i ? i : 6, void 0 !== t.alt ? [u(t.lng, i), u(t.lat, i), u(t.alt, i)] : [u(t.lng, i), u(t.lat, i)]
            }

            function je(t, i, e, n) {
                for (var o = [], s = 0, r = t.length; s < r; s++) o.push(i ? je(t[s], i - 1, e, n) : De(t[s], n));
                return !i && e && o.push(o[0]), o
            }

            function We(t, e) {
                return t.feature ? i({}, t.feature, {geometry: e}) : He(e)
            }

            function He(t) {
                return "Feature" === t.type || "FeatureCollection" === t.type ? t : {
                    type: "Feature",
                    properties: {},
                    geometry: t
                }
            }

            var Fe = {
                toGeoJSON: function (t) {
                    return We(this, {type: "Point", coordinates: De(this.getLatLng(), t)})
                }
            };

            function Ue(t, i) {
                return new Ae(t, i)
            }

            Ce.include(Fe), Ee.include(Fe), Ze.include(Fe), ke.include({
                toGeoJSON: function (t) {
                    var i = !ce(this._latlngs);
                    return We(this, {
                        type: (i ? "Multi" : "") + "LineString",
                        coordinates: je(this._latlngs, i ? 1 : 0, !1, t)
                    })
                }
            }), Be.include({
                toGeoJSON: function (t) {
                    var i = !ce(this._latlngs), e = i && !ce(this._latlngs[0]),
                        n = je(this._latlngs, e ? 2 : i ? 1 : 0, !0, t);
                    return i || (n = [n]), We(this, {type: (e ? "Multi" : "") + "Polygon", coordinates: n})
                }
            }), Le.include({
                toMultiPoint: function (t) {
                    var i = [];
                    return this.eachLayer(function (e) {
                        i.push(e.toGeoJSON(t).geometry.coordinates)
                    }), We(this, {type: "MultiPoint", coordinates: i})
                }, toGeoJSON: function (t) {
                    var i = this.feature && this.feature.geometry && this.feature.geometry.type;
                    if ("MultiPoint" === i) return this.toMultiPoint(t);
                    var e = "GeometryCollection" === i, n = [];
                    return this.eachLayer(function (i) {
                        if (i.toGeoJSON) {
                            var o = i.toGeoJSON(t);
                            if (e) n.push(o.geometry); else {
                                var s = He(o);
                                "FeatureCollection" === s.type ? n.push.apply(n, s.features) : n.push(s)
                            }
                        }
                    }), e ? We(this, {geometries: n, type: "GeometryCollection"}) : {
                        type: "FeatureCollection",
                        features: n
                    }
                }
            });
            var Ve = Ue, qe = Pe.extend({
                options: {
                    opacity: 1,
                    alt: "",
                    interactive: !1,
                    crossOrigin: !1,
                    errorOverlayUrl: "",
                    zIndex: 1,
                    className: ""
                }, initialize: function (t, i, e) {
                    this._url = t, this._bounds = R(i), _(this, e)
                }, onAdd: function () {
                    this._image || (this._initImage(), this.options.opacity < 1 && this._updateOpacity()), this.options.interactive && (ai(this._image, "leaflet-interactive"), this.addInteractiveTarget(this._image)), this.getPane().appendChild(this._image), this._reset()
                }, onRemove: function () {
                    ei(this._image), this.options.interactive && this.removeInteractiveTarget(this._image)
                }, setOpacity: function (t) {
                    return this.options.opacity = t, this._image && this._updateOpacity(), this
                }, setStyle: function (t) {
                    return t.opacity && this.setOpacity(t.opacity), this
                }, bringToFront: function () {
                    return this._map && oi(this._image), this
                }, bringToBack: function () {
                    return this._map && si(this._image), this
                }, setUrl: function (t) {
                    return this._url = t, this._image && (this._image.src = t), this
                }, setBounds: function (t) {
                    return this._bounds = R(t), this._map && this._reset(), this
                }, getEvents: function () {
                    var t = {zoom: this._reset, viewreset: this._reset};
                    return this._zoomAnimated && (t.zoomanim = this._animateZoom), t
                }, setZIndex: function (t) {
                    return this.options.zIndex = t, this._updateZIndex(), this
                }, getBounds: function () {
                    return this._bounds
                }, getElement: function () {
                    return this._image
                }, _initImage: function () {
                    var t = "IMG" === this._url.tagName, i = this._image = t ? this._url : ii("img");
                    ai(i, "leaflet-image-layer"), this._zoomAnimated && ai(i, "leaflet-zoom-animated"), this.options.className && ai(i, this.options.className), i.onselectstart = h, i.onmousemove = h, i.onload = n(this.fire, this, "load"), i.onerror = n(this._overlayOnError, this, "error"), (this.options.crossOrigin || "" === this.options.crossOrigin) && (i.crossOrigin = !0 === this.options.crossOrigin ? "" : this.options.crossOrigin), this.options.zIndex && this._updateZIndex(), t ? this._url = i.src : (i.src = this._url, i.alt = this.options.alt)
                }, _animateZoom: function (t) {
                    var i = this._map.getZoomScale(t.zoom),
                        e = this._map._latLngBoundsToNewLayerBounds(this._bounds, t.zoom, t.center).min;
                    di(this._image, e, i)
                }, _reset: function () {
                    var t = this._image,
                        i = new A(this._map.latLngToLayerPoint(this._bounds.getNorthWest()), this._map.latLngToLayerPoint(this._bounds.getSouthEast())),
                        e = i.getSize();
                    pi(t, i.min), t.style.width = e.x + "px", t.style.height = e.y + "px"
                }, _updateOpacity: function () {
                    ci(this._image, this.options.opacity)
                }, _updateZIndex: function () {
                    this._image && void 0 !== this.options.zIndex && null !== this.options.zIndex && (this._image.style.zIndex = this.options.zIndex)
                }, _overlayOnError: function () {
                    this.fire("error");
                    var t = this.options.errorOverlayUrl;
                    t && this._url !== t && (this._url = t, this._image.src = t)
                }
            }), Ge = qe.extend({
                options: {autoplay: !0, loop: !0, keepAspectRatio: !0, muted: !1},
                _initImage: function () {
                    var t = "VIDEO" === this._url.tagName, i = this._image = t ? this._url : ii("video");
                    if (ai(i, "leaflet-image-layer"), this._zoomAnimated && ai(i, "leaflet-zoom-animated"), this.options.className && ai(i, this.options.className), i.onselectstart = h, i.onmousemove = h, i.onloadeddata = n(this.fire, this, "load"), t) {
                        for (var e = i.getElementsByTagName("source"), o = [], s = 0; s < e.length; s++) o.push(e[s].src);
                        this._url = e.length > 0 ? o : [i.src]
                    } else {
                        f(this._url) || (this._url = [this._url]), !this.options.keepAspectRatio && Object.prototype.hasOwnProperty.call(i.style, "objectFit") && (i.style.objectFit = "fill"), i.autoplay = !!this.options.autoplay, i.loop = !!this.options.loop, i.muted = !!this.options.muted;
                        for (var r = 0; r < this._url.length; r++) {
                            var a = ii("source");
                            a.src = this._url[r], i.appendChild(a)
                        }
                    }
                }
            });
            var Ke = qe.extend({
                _initImage: function () {
                    var t = this._image = this._url;
                    ai(t, "leaflet-image-layer"), this._zoomAnimated && ai(t, "leaflet-zoom-animated"), this.options.className && ai(t, this.options.className), t.onselectstart = h, t.onmousemove = h
                }
            });
            var Ye = Pe.extend({
                options: {offset: [0, 7], className: "", pane: "popupPane"}, initialize: function (t, i) {
                    _(this, t), this._source = i
                }, onAdd: function (t) {
                    this._zoomAnimated = t._zoomAnimated, this._container || this._initLayout(), t._fadeAnimated && ci(this._container, 0), clearTimeout(this._removeTimeout), this.getPane().appendChild(this._container), this.update(), t._fadeAnimated && ci(this._container, 1), this.bringToFront()
                }, onRemove: function (t) {
                    t._fadeAnimated ? (ci(this._container, 0), this._removeTimeout = setTimeout(n(ei, void 0, this._container), 200)) : ei(this._container)
                }, getLatLng: function () {
                    return this._latlng
                }, setLatLng: function (t) {
                    return this._latlng = D(t), this._map && (this._updatePosition(), this._adjustPan()), this
                }, getContent: function () {
                    return this._content
                }, setContent: function (t) {
                    return this._content = t, this.update(), this
                }, getElement: function () {
                    return this._container
                }, update: function () {
                    this._map && (this._container.style.visibility = "hidden", this._updateContent(), this._updateLayout(), this._updatePosition(), this._container.style.visibility = "", this._adjustPan())
                }, getEvents: function () {
                    var t = {zoom: this._updatePosition, viewreset: this._updatePosition};
                    return this._zoomAnimated && (t.zoomanim = this._animateZoom), t
                }, isOpen: function () {
                    return !!this._map && this._map.hasLayer(this)
                }, bringToFront: function () {
                    return this._map && oi(this._container), this
                }, bringToBack: function () {
                    return this._map && si(this._container), this
                }, _prepareOpen: function (t, i, e) {
                    if (i instanceof Pe || (e = i, i = t), i instanceof be) for (var n in t._layers) {
                        i = t._layers[n];
                        break
                    }
                    if (!e) if (i.getCenter) e = i.getCenter(); else {
                        if (!i.getLatLng) throw new Error("Unable to get source layer LatLng.");
                        e = i.getLatLng()
                    }
                    return this._source = i, this.update(), e
                }, _updateContent: function () {
                    if (this._content) {
                        var t = this._contentNode,
                            i = "function" == typeof this._content ? this._content(this._source || this) : this._content;
                        if ("string" == typeof i) t.innerHTML = i; else {
                            for (; t.hasChildNodes();) t.removeChild(t.firstChild);
                            t.appendChild(i)
                        }
                        this.fire("contentupdate")
                    }
                }, _updatePosition: function () {
                    if (this._map) {
                        var t = this._map.latLngToLayerPoint(this._latlng), i = B(this.options.offset),
                            e = this._getAnchor();
                        this._zoomAnimated ? pi(this._container, t.add(e)) : i = i.add(t).add(e);
                        var n = this._containerBottom = -i.y,
                            o = this._containerLeft = -Math.round(this._containerWidth / 2) + i.x;
                        this._container.style.bottom = n + "px", this._container.style.left = o + "px"
                    }
                }, _getAnchor: function () {
                    return [0, 0]
                }
            }), Xe = Ye.extend({
                options: {
                    maxWidth: 300,
                    minWidth: 50,
                    maxHeight: null,
                    autoPan: !0,
                    autoPanPaddingTopLeft: null,
                    autoPanPaddingBottomRight: null,
                    autoPanPadding: [5, 5],
                    keepInView: !1,
                    closeButton: !0,
                    autoClose: !0,
                    closeOnEscapeKey: !0,
                    className: ""
                }, openOn: function (t) {
                    return t.openPopup(this), this
                }, onAdd: function (t) {
                    Ye.prototype.onAdd.call(this, t), t.fire("popupopen", {popup: this}), this._source && (this._source.fire("popupopen", {popup: this}, !0), this._source instanceof Se || this._source.on("preclick", Ei))
                }, onRemove: function (t) {
                    Ye.prototype.onRemove.call(this, t), t.fire("popupclose", {popup: this}), this._source && (this._source.fire("popupclose", {popup: this}, !0), this._source instanceof Se || this._source.off("preclick", Ei))
                }, getEvents: function () {
                    var t = Ye.prototype.getEvents.call(this);
                    return (void 0 !== this.options.closeOnClick ? this.options.closeOnClick : this._map.options.closePopupOnClick) && (t.preclick = this._close), this.options.keepInView && (t.moveend = this._adjustPan), t
                }, _close: function () {
                    this._map && this._map.closePopup(this)
                }, _initLayout: function () {
                    var t = "leaflet-popup",
                        i = this._container = ii("div", t + " " + (this.options.className || "") + " leaflet-zoom-animated"),
                        e = this._wrapper = ii("div", t + "-content-wrapper", i);
                    if (this._contentNode = ii("div", t + "-content", e), Bi(i), ki(this._contentNode), bi(i, "contextmenu", Ei), this._tipContainer = ii("div", t + "-tip-container", i), this._tip = ii("div", t + "-tip", this._tipContainer), this.options.closeButton) {
                        var n = this._closeButton = ii("a", t + "-close-button", i);
                        n.href = "#close", n.innerHTML = "&#215;", bi(n, "click", this._onCloseButtonClick, this)
                    }
                }, _updateLayout: function () {
                    var t = this._contentNode, i = t.style;
                    i.width = "", i.whiteSpace = "nowrap";
                    var e = t.offsetWidth;
                    e = Math.min(e, this.options.maxWidth), e = Math.max(e, this.options.minWidth), i.width = e + 1 + "px", i.whiteSpace = "", i.height = "";
                    var n = t.offsetHeight, o = this.options.maxHeight;
                    o && n > o ? (i.height = o + "px", ai(t, "leaflet-popup-scrolled")) : hi(t, "leaflet-popup-scrolled"), this._containerWidth = this._container.offsetWidth
                }, _animateZoom: function (t) {
                    var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center), e = this._getAnchor();
                    pi(this._container, i.add(e))
                }, _adjustPan: function () {
                    if (this.options.autoPan) {
                        this._map._panAnim && this._map._panAnim.stop();
                        var t = this._map, i = parseInt(ti(this._container, "marginBottom"), 10) || 0,
                            e = this._container.offsetHeight + i, n = this._containerWidth,
                            o = new E(this._containerLeft, -e - this._containerBottom);
                        o._add(mi(this._container));
                        var s = t.layerPointToContainerPoint(o), r = B(this.options.autoPanPadding),
                            a = B(this.options.autoPanPaddingTopLeft || r),
                            h = B(this.options.autoPanPaddingBottomRight || r), u = t.getSize(), l = 0, c = 0;
                        s.x + n + h.x > u.x && (l = s.x + n - u.x + h.x), s.x - l - a.x < 0 && (l = s.x - a.x), s.y + e + h.y > u.y && (c = s.y + e - u.y + h.y), s.y - c - a.y < 0 && (c = s.y - a.y), (l || c) && t.fire("autopanstart").panBy([l, c])
                    }
                }, _onCloseButtonClick: function (t) {
                    this._close(), Ii(t)
                }, _getAnchor: function () {
                    return B(this._source && this._source._getPopupAnchor ? this._source._getPopupAnchor() : [0, 0])
                }
            });
            Vi.mergeOptions({closePopupOnClick: !0}), Vi.include({
                openPopup: function (t, i, e) {
                    return t instanceof Xe || (t = new Xe(e).setContent(t)), i && t.setLatLng(i), this.hasLayer(t) ? this : (this._popup && this._popup.options.autoClose && this.closePopup(), this._popup = t, this.addLayer(t))
                }, closePopup: function (t) {
                    return t && t !== this._popup || (t = this._popup, this._popup = null), t && this.removeLayer(t), this
                }
            }), Pe.include({
                bindPopup: function (t, i) {
                    return t instanceof Xe ? (_(t, i), this._popup = t, t._source = this) : (this._popup && !i || (this._popup = new Xe(i, this)), this._popup.setContent(t)), this._popupHandlersAdded || (this.on({
                        click: this._openPopup,
                        keypress: this._onKeyPress,
                        remove: this.closePopup,
                        move: this._movePopup
                    }), this._popupHandlersAdded = !0), this
                }, unbindPopup: function () {
                    return this._popup && (this.off({
                        click: this._openPopup,
                        keypress: this._onKeyPress,
                        remove: this.closePopup,
                        move: this._movePopup
                    }), this._popupHandlersAdded = !1, this._popup = null), this
                }, openPopup: function (t, i) {
                    return this._popup && this._map && (i = this._popup._prepareOpen(this, t, i), this._map.openPopup(this._popup, i)), this
                }, closePopup: function () {
                    return this._popup && this._popup._close(), this
                }, togglePopup: function (t) {
                    return this._popup && (this._popup._map ? this.closePopup() : this.openPopup(t)), this
                }, isPopupOpen: function () {
                    return !!this._popup && this._popup.isOpen()
                }, setPopupContent: function (t) {
                    return this._popup && this._popup.setContent(t), this
                }, getPopup: function () {
                    return this._popup
                }, _openPopup: function (t) {
                    var i = t.layer || t.target;
                    this._popup && this._map && (Ii(t), i instanceof Se ? this.openPopup(t.layer || t.target, t.latlng) : this._map.hasLayer(this._popup) && this._popup._source === i ? this.closePopup() : this.openPopup(i, t.latlng))
                }, _movePopup: function (t) {
                    this._popup.setLatLng(t.latlng)
                }, _onKeyPress: function (t) {
                    13 === t.originalEvent.keyCode && this._openPopup(t)
                }
            });
            var Je = Ye.extend({
                options: {
                    pane: "tooltipPane",
                    offset: [0, 0],
                    direction: "auto",
                    permanent: !1,
                    sticky: !1,
                    interactive: !1,
                    opacity: .9
                }, onAdd: function (t) {
                    Ye.prototype.onAdd.call(this, t), this.setOpacity(this.options.opacity), t.fire("tooltipopen", {tooltip: this}), this._source && this._source.fire("tooltipopen", {tooltip: this}, !0)
                }, onRemove: function (t) {
                    Ye.prototype.onRemove.call(this, t), t.fire("tooltipclose", {tooltip: this}), this._source && this._source.fire("tooltipclose", {tooltip: this}, !0)
                }, getEvents: function () {
                    var t = Ye.prototype.getEvents.call(this);
                    return wt && !this.options.permanent && (t.preclick = this._close), t
                }, _close: function () {
                    this._map && this._map.closeTooltip(this)
                }, _initLayout: function () {
                    var t = "leaflet-tooltip " + (this.options.className || "") + " leaflet-zoom-" + (this._zoomAnimated ? "animated" : "hide");
                    this._contentNode = this._container = ii("div", t)
                }, _updateLayout: function () {
                }, _adjustPan: function () {
                }, _setPosition: function (t) {
                    var i, e, n = this._map, o = this._container, s = n.latLngToContainerPoint(n.getCenter()),
                        r = n.layerPointToContainerPoint(t), a = this.options.direction, h = o.offsetWidth,
                        u = o.offsetHeight, l = B(this.options.offset), c = this._getAnchor();
                    "top" === a ? (i = h / 2, e = u) : "bottom" === a ? (i = h / 2, e = 0) : "center" === a ? (i = h / 2, e = u / 2) : "right" === a ? (i = 0, e = u / 2) : "left" === a ? (i = h, e = u / 2) : r.x < s.x ? (a = "right", i = 0, e = u / 2) : (a = "left", i = h + 2 * (l.x + c.x), e = u / 2), t = t.subtract(B(i, e, !0)).add(l).add(c), hi(o, "leaflet-tooltip-right"), hi(o, "leaflet-tooltip-left"), hi(o, "leaflet-tooltip-top"), hi(o, "leaflet-tooltip-bottom"), ai(o, "leaflet-tooltip-" + a), pi(o, t)
                }, _updatePosition: function () {
                    var t = this._map.latLngToLayerPoint(this._latlng);
                    this._setPosition(t)
                }, setOpacity: function (t) {
                    this.options.opacity = t, this._container && ci(this._container, t)
                }, _animateZoom: function (t) {
                    var i = this._map._latLngToNewLayerPoint(this._latlng, t.zoom, t.center);
                    this._setPosition(i)
                }, _getAnchor: function () {
                    return B(this._source && this._source._getTooltipAnchor && !this.options.sticky ? this._source._getTooltipAnchor() : [0, 0])
                }
            });
            Vi.include({
                openTooltip: function (t, i, e) {
                    return t instanceof Je || (t = new Je(e).setContent(t)), i && t.setLatLng(i), this.hasLayer(t) ? this : this.addLayer(t)
                }, closeTooltip: function (t) {
                    return t && this.removeLayer(t), this
                }
            }), Pe.include({
                bindTooltip: function (t, i) {
                    return t instanceof Je ? (_(t, i), this._tooltip = t, t._source = this) : (this._tooltip && !i || (this._tooltip = new Je(i, this)), this._tooltip.setContent(t)), this._initTooltipInteractions(), this._tooltip.options.permanent && this._map && this._map.hasLayer(this) && this.openTooltip(), this
                }, unbindTooltip: function () {
                    return this._tooltip && (this._initTooltipInteractions(!0), this.closeTooltip(), this._tooltip = null), this
                }, _initTooltipInteractions: function (t) {
                    if (t || !this._tooltipHandlersAdded) {
                        var i = t ? "off" : "on", e = {remove: this.closeTooltip, move: this._moveTooltip};
                        this._tooltip.options.permanent ? e.add = this._openTooltip : (e.mouseover = this._openTooltip, e.mouseout = this.closeTooltip, this._tooltip.options.sticky && (e.mousemove = this._moveTooltip), wt && (e.click = this._openTooltip)), this[i](e), this._tooltipHandlersAdded = !t
                    }
                }, openTooltip: function (t, i) {
                    return this._tooltip && this._map && (i = this._tooltip._prepareOpen(this, t, i), this._map.openTooltip(this._tooltip, i), this._tooltip.options.interactive && this._tooltip._container && (ai(this._tooltip._container, "leaflet-clickable"), this.addInteractiveTarget(this._tooltip._container))), this
                }, closeTooltip: function () {
                    return this._tooltip && (this._tooltip._close(), this._tooltip.options.interactive && this._tooltip._container && (hi(this._tooltip._container, "leaflet-clickable"), this.removeInteractiveTarget(this._tooltip._container))), this
                }, toggleTooltip: function (t) {
                    return this._tooltip && (this._tooltip._map ? this.closeTooltip() : this.openTooltip(t)), this
                }, isTooltipOpen: function () {
                    return this._tooltip.isOpen()
                }, setTooltipContent: function (t) {
                    return this._tooltip && this._tooltip.setContent(t), this
                }, getTooltip: function () {
                    return this._tooltip
                }, _openTooltip: function (t) {
                    var i = t.layer || t.target;
                    this._tooltip && this._map && this.openTooltip(i, this._tooltip.options.sticky ? t.latlng : void 0)
                }, _moveTooltip: function (t) {
                    var i, e, n = t.latlng;
                    this._tooltip.options.sticky && t.originalEvent && (i = this._map.mouseEventToContainerPoint(t.originalEvent), e = this._map.containerPointToLayerPoint(i), n = this._map.layerPointToLatLng(e)), this._tooltip.setLatLng(n)
                }
            });
            var $e = Te.extend({
                options: {iconSize: [12, 12], html: !1, bgPos: null, className: "leaflet-div-icon"},
                createIcon: function (t) {
                    var i = t && "DIV" === t.tagName ? t : document.createElement("div"), e = this.options;
                    if (e.html instanceof Element ? (ni(i), i.appendChild(e.html)) : i.innerHTML = !1 !== e.html ? e.html : "", e.bgPos) {
                        var n = B(e.bgPos);
                        i.style.backgroundPosition = -n.x + "px " + -n.y + "px"
                    }
                    return this._setIconStyles(i, "icon"), i
                },
                createShadow: function () {
                    return null
                }
            });
            Te.Default = Me;
            var Qe = Pe.extend({
                options: {
                    tileSize: 256,
                    opacity: 1,
                    updateWhenIdle: ft,
                    updateWhenZooming: !0,
                    updateInterval: 200,
                    zIndex: 1,
                    bounds: null,
                    minZoom: 0,
                    maxZoom: void 0,
                    maxNativeZoom: void 0,
                    minNativeZoom: void 0,
                    noWrap: !1,
                    pane: "tilePane",
                    className: "",
                    keepBuffer: 2
                }, initialize: function (t) {
                    _(this, t)
                }, onAdd: function () {
                    this._initContainer(), this._levels = {}, this._tiles = {}, this._resetView(), this._update()
                }, beforeAdd: function (t) {
                    t._addZoomLimit(this)
                }, onRemove: function (t) {
                    this._removeAllTiles(), ei(this._container), t._removeZoomLimit(this), this._container = null, this._tileZoom = void 0
                }, bringToFront: function () {
                    return this._map && (oi(this._container), this._setAutoZIndex(Math.max)), this
                }, bringToBack: function () {
                    return this._map && (si(this._container), this._setAutoZIndex(Math.min)), this
                }, getContainer: function () {
                    return this._container
                }, setOpacity: function (t) {
                    return this.options.opacity = t, this._updateOpacity(), this
                }, setZIndex: function (t) {
                    return this.options.zIndex = t, this._updateZIndex(), this
                }, isLoading: function () {
                    return this._loading
                }, redraw: function () {
                    return this._map && (this._removeAllTiles(), this._update()), this
                }, getEvents: function () {
                    var t = {
                        viewprereset: this._invalidateAll,
                        viewreset: this._resetView,
                        zoom: this._resetView,
                        moveend: this._onMoveEnd
                    };
                    return this.options.updateWhenIdle || (this._onMove || (this._onMove = r(this._onMoveEnd, this.options.updateInterval, this)), t.move = this._onMove), this._zoomAnimated && (t.zoomanim = this._animateZoom), t
                }, createTile: function () {
                    return document.createElement("div")
                }, getTileSize: function () {
                    var t = this.options.tileSize;
                    return t instanceof E ? t : new E(t, t)
                }, _updateZIndex: function () {
                    this._container && void 0 !== this.options.zIndex && null !== this.options.zIndex && (this._container.style.zIndex = this.options.zIndex)
                }, _setAutoZIndex: function (t) {
                    for (var i, e = this.getPane().children, n = -t(-1 / 0, 1 / 0), o = 0, s = e.length; o < s; o++) i = e[o].style.zIndex, e[o] !== this._container && i && (n = t(n, +i));
                    isFinite(n) && (this.options.zIndex = n + t(-1, 1), this._updateZIndex())
                }, _updateOpacity: function () {
                    if (this._map && !$) {
                        ci(this._container, this.options.opacity);
                        var t = +new Date, i = !1, e = !1;
                        for (var n in this._tiles) {
                            var o = this._tiles[n];
                            if (o.current && o.loaded) {
                                var s = Math.min(1, (t - o.loaded) / 200);
                                ci(o.el, s), s < 1 ? i = !0 : (o.active ? e = !0 : this._onOpaqueTile(o), o.active = !0)
                            }
                        }
                        e && !this._noPrune && this._pruneTiles(), i && (M(this._fadeFrame), this._fadeFrame = T(this._updateOpacity, this))
                    }
                }, _onOpaqueTile: h, _initContainer: function () {
                    this._container || (this._container = ii("div", "leaflet-layer " + (this.options.className || "")), this._updateZIndex(), this.options.opacity < 1 && this._updateOpacity(), this.getPane().appendChild(this._container))
                }, _updateLevels: function () {
                    var t = this._tileZoom, i = this.options.maxZoom;
                    if (void 0 !== t) {
                        for (var e in this._levels) e = Number(e), this._levels[e].el.children.length || e === t ? (this._levels[e].el.style.zIndex = i - Math.abs(t - e), this._onUpdateLevel(e)) : (ei(this._levels[e].el), this._removeTilesAtZoom(e), this._onRemoveLevel(e), delete this._levels[e]);
                        var n = this._levels[t], o = this._map;
                        return n || ((n = this._levels[t] = {}).el = ii("div", "leaflet-tile-container leaflet-zoom-animated", this._container), n.el.style.zIndex = i, n.origin = o.project(o.unproject(o.getPixelOrigin()), t).round(), n.zoom = t, this._setZoomTransform(n, o.getCenter(), o.getZoom()), n.el.offsetWidth, this._onCreateLevel(n)), this._level = n, n
                    }
                }, _onUpdateLevel: h, _onRemoveLevel: h, _onCreateLevel: h, _pruneTiles: function () {
                    if (this._map) {
                        var t, i, e = this._map.getZoom();
                        if (e > this.options.maxZoom || e < this.options.minZoom) this._removeAllTiles(); else {
                            for (t in this._tiles) (i = this._tiles[t]).retain = i.current;
                            for (t in this._tiles) if ((i = this._tiles[t]).current && !i.active) {
                                var n = i.coords;
                                this._retainParent(n.x, n.y, n.z, n.z - 5) || this._retainChildren(n.x, n.y, n.z, n.z + 2)
                            }
                            for (t in this._tiles) this._tiles[t].retain || this._removeTile(t)
                        }
                    }
                }, _removeTilesAtZoom: function (t) {
                    for (var i in this._tiles) this._tiles[i].coords.z === t && this._removeTile(i)
                }, _removeAllTiles: function () {
                    for (var t in this._tiles) this._removeTile(t)
                }, _invalidateAll: function () {
                    for (var t in this._levels) ei(this._levels[t].el), this._onRemoveLevel(Number(t)), delete this._levels[t];
                    this._removeAllTiles(), this._tileZoom = void 0
                }, _retainParent: function (t, i, e, n) {
                    var o = Math.floor(t / 2), s = Math.floor(i / 2), r = e - 1, a = new E(+o, +s);
                    a.z = +r;
                    var h = this._tileCoordsToKey(a), u = this._tiles[h];
                    return u && u.active ? (u.retain = !0, !0) : (u && u.loaded && (u.retain = !0), r > n && this._retainParent(o, s, r, n))
                }, _retainChildren: function (t, i, e, n) {
                    for (var o = 2 * t; o < 2 * t + 2; o++) for (var s = 2 * i; s < 2 * i + 2; s++) {
                        var r = new E(o, s);
                        r.z = e + 1;
                        var a = this._tileCoordsToKey(r), h = this._tiles[a];
                        h && h.active ? h.retain = !0 : (h && h.loaded && (h.retain = !0), e + 1 < n && this._retainChildren(o, s, e + 1, n))
                    }
                }, _resetView: function (t) {
                    var i = t && (t.pinch || t.flyTo);
                    this._setView(this._map.getCenter(), this._map.getZoom(), i, i)
                }, _animateZoom: function (t) {
                    this._setView(t.center, t.zoom, !0, t.noUpdate)
                }, _clampZoom: function (t) {
                    var i = this.options;
                    return void 0 !== i.minNativeZoom && t < i.minNativeZoom ? i.minNativeZoom : void 0 !== i.maxNativeZoom && i.maxNativeZoom < t ? i.maxNativeZoom : t
                }, _setView: function (t, i, e, n) {
                    var o = Math.round(i);
                    o = void 0 !== this.options.maxZoom && o > this.options.maxZoom || void 0 !== this.options.minZoom && o < this.options.minZoom ? void 0 : this._clampZoom(o);
                    var s = this.options.updateWhenZooming && o !== this._tileZoom;
                    n && !s || (this._tileZoom = o, this._abortLoading && this._abortLoading(), this._updateLevels(), this._resetGrid(), void 0 !== o && this._update(t), e || this._pruneTiles(), this._noPrune = !!e), this._setZoomTransforms(t, i)
                }, _setZoomTransforms: function (t, i) {
                    for (var e in this._levels) this._setZoomTransform(this._levels[e], t, i)
                }, _setZoomTransform: function (t, i, e) {
                    var n = this._map.getZoomScale(e, t.zoom),
                        o = t.origin.multiplyBy(n).subtract(this._map._getNewPixelOrigin(i, e)).round();
                    mt ? di(t.el, o, n) : pi(t.el, o)
                }, _resetGrid: function () {
                    var t = this._map, i = t.options.crs, e = this._tileSize = this.getTileSize(), n = this._tileZoom,
                        o = this._map.getPixelWorldBounds(this._tileZoom);
                    o && (this._globalTileRange = this._pxBoundsToTileRange(o)), this._wrapX = i.wrapLng && !this.options.noWrap && [Math.floor(t.project([0, i.wrapLng[0]], n).x / e.x), Math.ceil(t.project([0, i.wrapLng[1]], n).x / e.y)], this._wrapY = i.wrapLat && !this.options.noWrap && [Math.floor(t.project([i.wrapLat[0], 0], n).y / e.x), Math.ceil(t.project([i.wrapLat[1], 0], n).y / e.y)]
                }, _onMoveEnd: function () {
                    this._map && !this._map._animatingZoom && this._update()
                }, _getTiledPixelBounds: function (t) {
                    var i = this._map, e = i._animatingZoom ? Math.max(i._animateToZoom, i.getZoom()) : i.getZoom(),
                        n = i.getZoomScale(e, this._tileZoom), o = i.project(t, this._tileZoom).floor(),
                        s = i.getSize().divideBy(2 * n);
                    return new A(o.subtract(s), o.add(s))
                }, _update: function (t) {
                    var i = this._map;
                    if (i) {
                        var e = this._clampZoom(i.getZoom());
                        if (void 0 === t && (t = i.getCenter()), void 0 !== this._tileZoom) {
                            var n = this._getTiledPixelBounds(t), o = this._pxBoundsToTileRange(n), s = o.getCenter(),
                                r = [], a = this.options.keepBuffer,
                                h = new A(o.getBottomLeft().subtract([a, -a]), o.getTopRight().add([a, -a]));
                            if (!(isFinite(o.min.x) && isFinite(o.min.y) && isFinite(o.max.x) && isFinite(o.max.y))) throw new Error("Attempted to load an infinite number of tiles");
                            for (var u in this._tiles) {
                                var l = this._tiles[u].coords;
                                l.z === this._tileZoom && h.contains(new E(l.x, l.y)) || (this._tiles[u].current = !1)
                            }
                            if (Math.abs(e - this._tileZoom) > 1) this._setView(t, e); else {
                                for (var c = o.min.y; c <= o.max.y; c++) for (var _ = o.min.x; _ <= o.max.x; _++) {
                                    var d = new E(_, c);
                                    if (d.z = this._tileZoom, this._isValidTile(d)) {
                                        var p = this._tiles[this._tileCoordsToKey(d)];
                                        p ? p.current = !0 : r.push(d)
                                    }
                                }
                                if (r.sort(function (t, i) {
                                    return t.distanceTo(s) - i.distanceTo(s)
                                }), 0 !== r.length) {
                                    this._loading || (this._loading = !0, this.fire("loading"));
                                    var m = document.createDocumentFragment();
                                    for (_ = 0; _ < r.length; _++) this._addTile(r[_], m);
                                    this._level.el.appendChild(m)
                                }
                            }
                        }
                    }
                }, _isValidTile: function (t) {
                    var i = this._map.options.crs;
                    if (!i.infinite) {
                        var e = this._globalTileRange;
                        if (!i.wrapLng && (t.x < e.min.x || t.x > e.max.x) || !i.wrapLat && (t.y < e.min.y || t.y > e.max.y)) return !1
                    }
                    if (!this.options.bounds) return !0;
                    var n = this._tileCoordsToBounds(t);
                    return R(this.options.bounds).overlaps(n)
                }, _keyToBounds: function (t) {
                    return this._tileCoordsToBounds(this._keyToTileCoords(t))
                }, _tileCoordsToNwSe: function (t) {
                    var i = this._map, e = this.getTileSize(), n = t.scaleBy(e), o = n.add(e);
                    return [i.unproject(n, t.z), i.unproject(o, t.z)]
                }, _tileCoordsToBounds: function (t) {
                    var i = this._tileCoordsToNwSe(t), e = new O(i[0], i[1]);
                    return this.options.noWrap || (e = this._map.wrapLatLngBounds(e)), e
                }, _tileCoordsToKey: function (t) {
                    return t.x + ":" + t.y + ":" + t.z
                }, _keyToTileCoords: function (t) {
                    var i = t.split(":"), e = new E(+i[0], +i[1]);
                    return e.z = +i[2], e
                }, _removeTile: function (t) {
                    var i = this._tiles[t];
                    i && (ei(i.el), delete this._tiles[t], this.fire("tileunload", {
                        tile: i.el,
                        coords: this._keyToTileCoords(t)
                    }))
                }, _initTile: function (t) {
                    ai(t, "leaflet-tile");
                    var i = this.getTileSize();
                    t.style.width = i.x + "px", t.style.height = i.y + "px", t.onselectstart = h, t.onmousemove = h, $ && this.options.opacity < 1 && ci(t, this.options.opacity), it && !et && (t.style.WebkitBackfaceVisibility = "hidden")
                }, _addTile: function (t, i) {
                    var e = this._getTilePos(t), o = this._tileCoordsToKey(t),
                        s = this.createTile(this._wrapCoords(t), n(this._tileReady, this, t));
                    this._initTile(s), this.createTile.length < 2 && T(n(this._tileReady, this, t, null, s)), pi(s, e), this._tiles[o] = {
                        el: s,
                        coords: t,
                        current: !0
                    }, i.appendChild(s), this.fire("tileloadstart", {tile: s, coords: t})
                }, _tileReady: function (t, i, e) {
                    i && this.fire("tileerror", {error: i, tile: e, coords: t});
                    var o = this._tileCoordsToKey(t);
                    (e = this._tiles[o]) && (e.loaded = +new Date, this._map._fadeAnimated ? (ci(e.el, 0), M(this._fadeFrame), this._fadeFrame = T(this._updateOpacity, this)) : (e.active = !0, this._pruneTiles()), i || (ai(e.el, "leaflet-tile-loaded"), this.fire("tileload", {
                        tile: e.el,
                        coords: t
                    })), this._noTilesToLoad() && (this._loading = !1, this.fire("load"), $ || !this._map._fadeAnimated ? T(this._pruneTiles, this) : setTimeout(n(this._pruneTiles, this), 250)))
                }, _getTilePos: function (t) {
                    return t.scaleBy(this.getTileSize()).subtract(this._level.origin)
                }, _wrapCoords: function (t) {
                    var i = new E(this._wrapX ? a(t.x, this._wrapX) : t.x, this._wrapY ? a(t.y, this._wrapY) : t.y);
                    return i.z = t.z, i
                }, _pxBoundsToTileRange: function (t) {
                    var i = this.getTileSize();
                    return new A(t.min.unscaleBy(i).floor(), t.max.unscaleBy(i).ceil().subtract([1, 1]))
                }, _noTilesToLoad: function () {
                    for (var t in this._tiles) if (!this._tiles[t].loaded) return !1;
                    return !0
                }
            });
            var tn = Qe.extend({
                options: {
                    minZoom: 0,
                    maxZoom: 18,
                    subdomains: "abc",
                    errorTileUrl: "",
                    zoomOffset: 0,
                    tms: !1,
                    zoomReverse: !1,
                    detectRetina: !1,
                    crossOrigin: !1
                }, initialize: function (t, i) {
                    this._url = t, (i = _(this, i)).detectRetina && bt && i.maxZoom > 0 && (i.tileSize = Math.floor(i.tileSize / 2), i.zoomReverse ? (i.zoomOffset--, i.minZoom++) : (i.zoomOffset++, i.maxZoom--), i.minZoom = Math.max(0, i.minZoom)), "string" == typeof i.subdomains && (i.subdomains = i.subdomains.split("")), it || this.on("tileunload", this._onTileRemove)
                }, setUrl: function (t, i) {
                    return this._url === t && void 0 === i && (i = !0), this._url = t, i || this.redraw(), this
                }, createTile: function (t, i) {
                    var e = document.createElement("img");
                    return bi(e, "load", n(this._tileOnLoad, this, i, e)), bi(e, "error", n(this._tileOnError, this, i, e)), (this.options.crossOrigin || "" === this.options.crossOrigin) && (e.crossOrigin = !0 === this.options.crossOrigin ? "" : this.options.crossOrigin), e.alt = "", e.setAttribute("role", "presentation"), e.src = this.getTileUrl(t), e
                }, getTileUrl: function (t) {
                    var e = {r: bt ? "@2x" : "", s: this._getSubdomain(t), x: t.x, y: t.y, z: this._getZoomForUrl()};
                    if (this._map && !this._map.options.crs.infinite) {
                        var n = this._globalTileRange.max.y - t.y;
                        this.options.tms && (e.y = n), e["-y"] = n
                    }
                    return m(this._url, i(e, this.options))
                }, _tileOnLoad: function (t, i) {
                    $ ? setTimeout(n(t, this, null, i), 0) : t(null, i)
                }, _tileOnError: function (t, i, e) {
                    var n = this.options.errorTileUrl;
                    n && i.getAttribute("src") !== n && (i.src = n), t(e, i)
                }, _onTileRemove: function (t) {
                    t.tile.onload = null
                }, _getZoomForUrl: function () {
                    var t = this._tileZoom, i = this.options.maxZoom;
                    return this.options.zoomReverse && (t = i - t), t + this.options.zoomOffset
                }, _getSubdomain: function (t) {
                    var i = Math.abs(t.x + t.y) % this.options.subdomains.length;
                    return this.options.subdomains[i]
                }, _abortLoading: function () {
                    var t, i;
                    for (t in this._tiles) this._tiles[t].coords.z !== this._tileZoom && ((i = this._tiles[t].el).onload = h, i.onerror = h, i.complete || (i.src = v, ei(i), delete this._tiles[t]))
                }, _removeTile: function (t) {
                    var i = this._tiles[t];
                    if (i) return ot || i.el.setAttribute("src", v), Qe.prototype._removeTile.call(this, t)
                }, _tileReady: function (t, i, e) {
                    if (this._map && (!e || e.getAttribute("src") !== v)) return Qe.prototype._tileReady.call(this, t, i, e)
                }
            });

            function en(t, i) {
                return new tn(t, i)
            }

            var nn = tn.extend({
                defaultWmsParams: {
                    service: "WMS",
                    request: "GetMap",
                    layers: "",
                    styles: "",
                    format: "image/jpeg",
                    transparent: !1,
                    version: "1.1.1"
                }, options: {crs: null, uppercase: !1}, initialize: function (t, e) {
                    this._url = t;
                    var n = i({}, this.defaultWmsParams);
                    for (var o in e) o in this.options || (n[o] = e[o]);
                    var s = (e = _(this, e)).detectRetina && bt ? 2 : 1, r = this.getTileSize();
                    n.width = r.x * s, n.height = r.y * s, this.wmsParams = n
                }, onAdd: function (t) {
                    this._crs = this.options.crs || t.options.crs, this._wmsVersion = parseFloat(this.wmsParams.version);
                    var i = this._wmsVersion >= 1.3 ? "crs" : "srs";
                    this.wmsParams[i] = this._crs.code, tn.prototype.onAdd.call(this, t)
                }, getTileUrl: function (t) {
                    var i = this._tileCoordsToNwSe(t), e = this._crs, n = I(e.project(i[0]), e.project(i[1])),
                        o = n.min, s = n.max,
                        r = (this._wmsVersion >= 1.3 && this._crs === xe ? [o.y, o.x, s.y, s.x] : [o.x, o.y, s.x, s.y]).join(","),
                        a = tn.prototype.getTileUrl.call(this, t);
                    return a + d(this.wmsParams, a, this.options.uppercase) + (this.options.uppercase ? "&BBOX=" : "&bbox=") + r
                }, setParams: function (t, e) {
                    return i(this.wmsParams, t), e || this.redraw(), this
                }
            });
            tn.WMS = nn, en.wms = function (t, i) {
                return new nn(t, i)
            };
            var on = Pe.extend({
                options: {padding: .1, tolerance: 0}, initialize: function (t) {
                    _(this, t), s(this), this._layers = this._layers || {}
                }, onAdd: function () {
                    this._container || (this._initContainer(), this._zoomAnimated && ai(this._container, "leaflet-zoom-animated")), this.getPane().appendChild(this._container), this._update(), this.on("update", this._updatePaths, this)
                }, onRemove: function () {
                    this.off("update", this._updatePaths, this), this._destroyContainer()
                }, getEvents: function () {
                    var t = {
                        viewreset: this._reset,
                        zoom: this._onZoom,
                        moveend: this._update,
                        zoomend: this._onZoomEnd
                    };
                    return this._zoomAnimated && (t.zoomanim = this._onAnimZoom), t
                }, _onAnimZoom: function (t) {
                    this._updateTransform(t.center, t.zoom)
                }, _onZoom: function () {
                    this._updateTransform(this._map.getCenter(), this._map.getZoom())
                }, _updateTransform: function (t, i) {
                    var e = this._map.getZoomScale(i, this._zoom), n = mi(this._container),
                        o = this._map.getSize().multiplyBy(.5 + this.options.padding),
                        s = this._map.project(this._center, i), r = this._map.project(t, i).subtract(s),
                        a = o.multiplyBy(-e).add(n).add(o).subtract(r);
                    mt ? di(this._container, a, e) : pi(this._container, a)
                }, _reset: function () {
                    for (var t in this._update(), this._updateTransform(this._center, this._zoom), this._layers) this._layers[t]._reset()
                }, _onZoomEnd: function () {
                    for (var t in this._layers) this._layers[t]._project()
                }, _updatePaths: function () {
                    for (var t in this._layers) this._layers[t]._update()
                }, _update: function () {
                    var t = this.options.padding, i = this._map.getSize(),
                        e = this._map.containerPointToLayerPoint(i.multiplyBy(-t)).round();
                    this._bounds = new A(e, e.add(i.multiplyBy(1 + 2 * t)).round()), this._center = this._map.getCenter(), this._zoom = this._map.getZoom()
                }
            }), sn = on.extend({
                getEvents: function () {
                    var t = on.prototype.getEvents.call(this);
                    return t.viewprereset = this._onViewPreReset, t
                }, _onViewPreReset: function () {
                    this._postponeUpdatePaths = !0
                }, onAdd: function () {
                    on.prototype.onAdd.call(this), this._draw()
                }, _initContainer: function () {
                    var t = this._container = document.createElement("canvas");
                    bi(t, "mousemove", this._onMouseMove, this), bi(t, "click dblclick mousedown mouseup contextmenu", this._onClick, this), bi(t, "mouseout", this._handleMouseOut, this), this._ctx = t.getContext("2d")
                }, _destroyContainer: function () {
                    M(this._redrawRequest), delete this._ctx, ei(this._container), Mi(this._container), delete this._container
                }, _updatePaths: function () {
                    if (!this._postponeUpdatePaths) {
                        for (var t in this._redrawBounds = null, this._layers) this._layers[t]._update();
                        this._redraw()
                    }
                }, _update: function () {
                    if (!this._map._animatingZoom || !this._bounds) {
                        on.prototype._update.call(this);
                        var t = this._bounds, i = this._container, e = t.getSize(), n = bt ? 2 : 1;
                        pi(i, t.min), i.width = n * e.x, i.height = n * e.y, i.style.width = e.x + "px", i.style.height = e.y + "px", bt && this._ctx.scale(2, 2), this._ctx.translate(-t.min.x, -t.min.y), this.fire("update")
                    }
                }, _reset: function () {
                    on.prototype._reset.call(this), this._postponeUpdatePaths && (this._postponeUpdatePaths = !1, this._updatePaths())
                }, _initPath: function (t) {
                    this._updateDashArray(t), this._layers[s(t)] = t;
                    var i = t._order = {layer: t, prev: this._drawLast, next: null};
                    this._drawLast && (this._drawLast.next = i), this._drawLast = i, this._drawFirst = this._drawFirst || this._drawLast
                }, _addPath: function (t) {
                    this._requestRedraw(t)
                }, _removePath: function (t) {
                    var i = t._order, e = i.next, n = i.prev;
                    e ? e.prev = n : this._drawLast = n, n ? n.next = e : this._drawFirst = e, delete t._order, delete this._layers[s(t)], this._requestRedraw(t)
                }, _updatePath: function (t) {
                    this._extendRedrawBounds(t), t._project(), t._update(), this._requestRedraw(t)
                }, _updateStyle: function (t) {
                    this._updateDashArray(t), this._requestRedraw(t)
                }, _updateDashArray: function (t) {
                    if ("string" == typeof t.options.dashArray) {
                        var i, e, n = t.options.dashArray.split(/[, ]+/), o = [];
                        for (e = 0; e < n.length; e++) {
                            if (i = Number(n[e]), isNaN(i)) return;
                            o.push(i)
                        }
                        t.options._dashArray = o
                    } else t.options._dashArray = t.options.dashArray
                }, _requestRedraw: function (t) {
                    this._map && (this._extendRedrawBounds(t), this._redrawRequest = this._redrawRequest || T(this._redraw, this))
                }, _extendRedrawBounds: function (t) {
                    if (t._pxBounds) {
                        var i = (t.options.weight || 0) + 1;
                        this._redrawBounds = this._redrawBounds || new A, this._redrawBounds.extend(t._pxBounds.min.subtract([i, i])), this._redrawBounds.extend(t._pxBounds.max.add([i, i]))
                    }
                }, _redraw: function () {
                    this._redrawRequest = null, this._redrawBounds && (this._redrawBounds.min._floor(), this._redrawBounds.max._ceil()), this._clear(), this._draw(), this._redrawBounds = null
                }, _clear: function () {
                    var t = this._redrawBounds;
                    if (t) {
                        var i = t.getSize();
                        this._ctx.clearRect(t.min.x, t.min.y, i.x, i.y)
                    } else this._ctx.save(), this._ctx.setTransform(1, 0, 0, 1, 0, 0), this._ctx.clearRect(0, 0, this._container.width, this._container.height), this._ctx.restore()
                }, _draw: function () {
                    var t, i = this._redrawBounds;
                    if (this._ctx.save(), i) {
                        var e = i.getSize();
                        this._ctx.beginPath(), this._ctx.rect(i.min.x, i.min.y, e.x, e.y), this._ctx.clip()
                    }
                    this._drawing = !0;
                    for (var n = this._drawFirst; n; n = n.next) t = n.layer, (!i || t._pxBounds && t._pxBounds.intersects(i)) && t._updatePath();
                    this._drawing = !1, this._ctx.restore()
                }, _updatePoly: function (t, i) {
                    if (this._drawing) {
                        var e, n, o, s, r = t._parts, a = r.length, h = this._ctx;
                        if (a) {
                            for (h.beginPath(), e = 0; e < a; e++) {
                                for (n = 0, o = r[e].length; n < o; n++) s = r[e][n], h[n ? "lineTo" : "moveTo"](s.x, s.y);
                                i && h.closePath()
                            }
                            this._fillStroke(h, t)
                        }
                    }
                }, _updateCircle: function (t) {
                    if (this._drawing && !t._empty()) {
                        var i = t._point, e = this._ctx, n = Math.max(Math.round(t._radius), 1),
                            o = (Math.max(Math.round(t._radiusY), 1) || n) / n;
                        1 !== o && (e.save(), e.scale(1, o)), e.beginPath(), e.arc(i.x, i.y / o, n, 0, 2 * Math.PI, !1), 1 !== o && e.restore(), this._fillStroke(e, t)
                    }
                }, _fillStroke: function (t, i) {
                    var e = i.options;
                    e.fill && (t.globalAlpha = e.fillOpacity, t.fillStyle = e.fillColor || e.color, t.fill(e.fillRule || "evenodd")), e.stroke && 0 !== e.weight && (t.setLineDash && t.setLineDash(i.options && i.options._dashArray || []), t.globalAlpha = e.opacity, t.lineWidth = e.weight, t.strokeStyle = e.color, t.lineCap = e.lineCap, t.lineJoin = e.lineJoin, t.stroke())
                }, _onClick: function (t) {
                    for (var i, e, n = this._map.mouseEventToLayerPoint(t), o = this._drawFirst; o; o = o.next) (i = o.layer).options.interactive && i._containsPoint(n) && ("click" !== t.type && "preclick" === t.type || !this._map._draggableMoved(i)) && (e = i);
                    e && (ji(t), this._fireEvent([e], t))
                }, _onMouseMove: function (t) {
                    if (this._map && !this._map.dragging.moving() && !this._map._animatingZoom) {
                        var i = this._map.mouseEventToLayerPoint(t);
                        this._handleMouseHover(t, i)
                    }
                }, _handleMouseOut: function (t) {
                    var i = this._hoveredLayer;
                    i && (hi(this._container, "leaflet-interactive"), this._fireEvent([i], t, "mouseout"), this._hoveredLayer = null, this._mouseHoverThrottled = !1)
                }, _handleMouseHover: function (t, i) {
                    if (!this._mouseHoverThrottled) {
                        for (var e, o, s = this._drawFirst; s; s = s.next) (e = s.layer).options.interactive && e._containsPoint(i) && (o = e);
                        o !== this._hoveredLayer && (this._handleMouseOut(t), o && (ai(this._container, "leaflet-interactive"), this._fireEvent([o], t, "mouseover"), this._hoveredLayer = o)), this._hoveredLayer && this._fireEvent([this._hoveredLayer], t), this._mouseHoverThrottled = !0, setTimeout(n(function () {
                            this._mouseHoverThrottled = !1
                        }, this), 32)
                    }
                }, _fireEvent: function (t, i, e) {
                    this._map._fireDOMEvent(i, e || i.type, t)
                }, _bringToFront: function (t) {
                    var i = t._order;
                    if (i) {
                        var e = i.next, n = i.prev;
                        e && (e.prev = n, n ? n.next = e : e && (this._drawFirst = e), i.prev = this._drawLast, this._drawLast.next = i, i.next = null, this._drawLast = i, this._requestRedraw(t))
                    }
                }, _bringToBack: function (t) {
                    var i = t._order;
                    if (i) {
                        var e = i.next, n = i.prev;
                        n && (n.next = e, e ? e.prev = n : n && (this._drawLast = n), i.prev = null, i.next = this._drawFirst, this._drawFirst.prev = i, this._drawFirst = i, this._requestRedraw(t))
                    }
                }
            });

            function rn(t) {
                return Mt ? new sn(t) : null
            }

            var an = function () {
                try {
                    return document.namespaces.add("lvml", "urn:schemas-microsoft-com:vml"), function (t) {
                        return document.createElement("<lvml:" + t + ' class="lvml">')
                    }
                } catch (t) {
                    return function (t) {
                        return document.createElement("<" + t + ' xmlns="urn:schemas-microsoft.com:vml" class="lvml">')
                    }
                }
            }(), hn = {
                _initContainer: function () {
                    this._container = ii("div", "leaflet-vml-container")
                }, _update: function () {
                    this._map._animatingZoom || (on.prototype._update.call(this), this.fire("update"))
                }, _initPath: function (t) {
                    var i = t._container = an("shape");
                    ai(i, "leaflet-vml-shape " + (this.options.className || "")), i.coordsize = "1 1", t._path = an("path"), i.appendChild(t._path), this._updateStyle(t), this._layers[s(t)] = t
                }, _addPath: function (t) {
                    var i = t._container;
                    this._container.appendChild(i), t.options.interactive && t.addInteractiveTarget(i)
                }, _removePath: function (t) {
                    var i = t._container;
                    ei(i), t.removeInteractiveTarget(i), delete this._layers[s(t)]
                }, _updateStyle: function (t) {
                    var i = t._stroke, e = t._fill, n = t.options, o = t._container;
                    o.stroked = !!n.stroke, o.filled = !!n.fill, n.stroke ? (i || (i = t._stroke = an("stroke")), o.appendChild(i), i.weight = n.weight + "px", i.color = n.color, i.opacity = n.opacity, n.dashArray ? i.dashStyle = f(n.dashArray) ? n.dashArray.join(" ") : n.dashArray.replace(/( *, *)/g, " ") : i.dashStyle = "", i.endcap = n.lineCap.replace("butt", "flat"), i.joinstyle = n.lineJoin) : i && (o.removeChild(i), t._stroke = null), n.fill ? (e || (e = t._fill = an("fill")), o.appendChild(e), e.color = n.fillColor || n.color, e.opacity = n.fillOpacity) : e && (o.removeChild(e), t._fill = null)
                }, _updateCircle: function (t) {
                    var i = t._point.round(), e = Math.round(t._radius), n = Math.round(t._radiusY || e);
                    this._setPath(t, t._empty() ? "M0 0" : "AL " + i.x + "," + i.y + " " + e + "," + n + " 0,23592600")
                }, _setPath: function (t, i) {
                    t._path.v = i
                }, _bringToFront: function (t) {
                    oi(t._container)
                }, _bringToBack: function (t) {
                    si(t._container)
                }
            }, un = Ct ? an : K, ln = on.extend({
                getEvents: function () {
                    var t = on.prototype.getEvents.call(this);
                    return t.zoomstart = this._onZoomStart, t
                }, _initContainer: function () {
                    this._container = un("svg"), this._container.setAttribute("pointer-events", "none"), this._rootGroup = un("g"), this._container.appendChild(this._rootGroup)
                }, _destroyContainer: function () {
                    ei(this._container), Mi(this._container), delete this._container, delete this._rootGroup, delete this._svgSize
                }, _onZoomStart: function () {
                    this._update()
                }, _update: function () {
                    if (!this._map._animatingZoom || !this._bounds) {
                        on.prototype._update.call(this);
                        var t = this._bounds, i = t.getSize(), e = this._container;
                        this._svgSize && this._svgSize.equals(i) || (this._svgSize = i, e.setAttribute("width", i.x), e.setAttribute("height", i.y)), pi(e, t.min), e.setAttribute("viewBox", [t.min.x, t.min.y, i.x, i.y].join(" ")), this.fire("update")
                    }
                }, _initPath: function (t) {
                    var i = t._path = un("path");
                    t.options.className && ai(i, t.options.className), t.options.interactive && ai(i, "leaflet-interactive"), this._updateStyle(t), this._layers[s(t)] = t
                }, _addPath: function (t) {
                    this._rootGroup || this._initContainer(), this._rootGroup.appendChild(t._path), t.addInteractiveTarget(t._path)
                }, _removePath: function (t) {
                    ei(t._path), t.removeInteractiveTarget(t._path), delete this._layers[s(t)]
                }, _updatePath: function (t) {
                    t._project(), t._update()
                }, _updateStyle: function (t) {
                    var i = t._path, e = t.options;
                    i && (e.stroke ? (i.setAttribute("stroke", e.color), i.setAttribute("stroke-opacity", e.opacity), i.setAttribute("stroke-width", e.weight), i.setAttribute("stroke-linecap", e.lineCap), i.setAttribute("stroke-linejoin", e.lineJoin), e.dashArray ? i.setAttribute("stroke-dasharray", e.dashArray) : i.removeAttribute("stroke-dasharray"), e.dashOffset ? i.setAttribute("stroke-dashoffset", e.dashOffset) : i.removeAttribute("stroke-dashoffset")) : i.setAttribute("stroke", "none"), e.fill ? (i.setAttribute("fill", e.fillColor || e.color), i.setAttribute("fill-opacity", e.fillOpacity), i.setAttribute("fill-rule", e.fillRule || "evenodd")) : i.setAttribute("fill", "none"))
                }, _updatePoly: function (t, i) {
                    this._setPath(t, Y(t._parts, i))
                }, _updateCircle: function (t) {
                    var i = t._point, e = Math.max(Math.round(t._radius), 1),
                        n = "a" + e + "," + (Math.max(Math.round(t._radiusY), 1) || e) + " 0 1,0 ",
                        o = t._empty() ? "M0 0" : "M" + (i.x - e) + "," + i.y + n + 2 * e + ",0 " + n + 2 * -e + ",0 ";
                    this._setPath(t, o)
                }, _setPath: function (t, i) {
                    t._path.setAttribute("d", i)
                }, _bringToFront: function (t) {
                    oi(t._path)
                }, _bringToBack: function (t) {
                    si(t._path)
                }
            });

            function cn(t) {
                return zt || Ct ? new ln(t) : null
            }

            Ct && ln.include(hn), Vi.include({
                getRenderer: function (t) {
                    var i = t.options.renderer || this._getPaneRenderer(t.options.pane) || this.options.renderer || this._renderer;
                    return i || (i = this._renderer = this._createRenderer()), this.hasLayer(i) || this.addLayer(i), i
                }, _getPaneRenderer: function (t) {
                    if ("overlayPane" === t || void 0 === t) return !1;
                    var i = this._paneRenderers[t];
                    return void 0 === i && (i = this._createRenderer({pane: t}), this._paneRenderers[t] = i), i
                }, _createRenderer: function (t) {
                    return this.options.preferCanvas && rn(t) || cn(t)
                }
            });
            var _n = Be.extend({
                initialize: function (t, i) {
                    Be.prototype.initialize.call(this, this._boundsToLatLngs(t), i)
                }, setBounds: function (t) {
                    return this.setLatLngs(this._boundsToLatLngs(t))
                }, _boundsToLatLngs: function (t) {
                    return [(t = R(t)).getSouthWest(), t.getNorthWest(), t.getNorthEast(), t.getSouthEast()]
                }
            });
            ln.create = un, ln.pointsToPath = Y, Ae.geometryToLayer = Ie, Ae.coordsToLatLng = Re, Ae.coordsToLatLngs = Ne, Ae.latLngToCoords = De, Ae.latLngsToCoords = je, Ae.getFeature = We, Ae.asFeature = He, Vi.mergeOptions({boxZoom: !0});
            var dn = $i.extend({
                initialize: function (t) {
                    try {
                        this._map = t, this._container = t._container, this._pane = t._panes.overlayPane, this._resetStateTimeout = 0, t.on("unload", this._destroy, this)
                    }catch (e) {

                    }

                }, addHooks: function () {
                    bi(this._container, "mousedown", this._onMouseDown, this)
                }, removeHooks: function () {
                    Mi(this._container, "mousedown", this._onMouseDown, this)
                }, moved: function () {
                    return this._moved
                }, _destroy: function () {
                    ei(this._pane), delete this._pane
                }, _resetState: function () {
                    this._resetStateTimeout = 0, this._moved = !1
                }, _clearDeferredResetState: function () {
                    0 !== this._resetStateTimeout && (clearTimeout(this._resetStateTimeout), this._resetStateTimeout = 0)
                }, _onMouseDown: function (t) {
                    if (!t.shiftKey || 1 !== t.which && 1 !== t.button) return !1;
                    this._clearDeferredResetState(), this._resetState(), Vt(), gi(), this._startPoint = this._map.mouseEventToContainerPoint(t), bi(document, {
                        contextmenu: Ii,
                        mousemove: this._onMouseMove,
                        mouseup: this._onMouseUp,
                        keydown: this._onKeyDown
                    }, this)
                }, _onMouseMove: function (t) {
                    this._moved || (this._moved = !0, this._box = ii("div", "leaflet-zoom-box", this._container), ai(this._container, "leaflet-crosshair"), this._map.fire("boxzoomstart")), this._point = this._map.mouseEventToContainerPoint(t);
                    var i = new A(this._point, this._startPoint), e = i.getSize();
                    pi(this._box, i.min), this._box.style.width = e.x + "px", this._box.style.height = e.y + "px"
                }, _finish: function () {
                    this._moved && (ei(this._box), hi(this._container, "leaflet-crosshair")), qt(), vi(), Mi(document, {
                        contextmenu: Ii,
                        mousemove: this._onMouseMove,
                        mouseup: this._onMouseUp,
                        keydown: this._onKeyDown
                    }, this)
                }, _onMouseUp: function (t) {
                    if ((1 === t.which || 1 === t.button) && (this._finish(), this._moved)) {
                        this._clearDeferredResetState(), this._resetStateTimeout = setTimeout(n(this._resetState, this), 0);
                        var i = new O(this._map.containerPointToLatLng(this._startPoint), this._map.containerPointToLatLng(this._point));
                        this._map.fitBounds(i).fire("boxzoomend", {boxZoomBounds: i})
                    }
                }, _onKeyDown: function (t) {
                    27 === t.keyCode && this._finish()
                }
            });
            Vi.addInitHook("addHandler", "boxZoom", dn), Vi.mergeOptions({doubleClickZoom: !0});
            var pn = $i.extend({
                addHooks: function () {
                    this._map.on("dblclick", this._onDoubleClick, this)
                }, removeHooks: function () {
                    this._map.off("dblclick", this._onDoubleClick, this)
                }, _onDoubleClick: function (t) {
                    var i = this._map, e = i.getZoom(), n = i.options.zoomDelta,
                        o = t.originalEvent.shiftKey ? e - n : e + n;
                    "center" === i.options.doubleClickZoom ? i.setZoom(o) : i.setZoomAround(t.containerPoint, o)
                }
            });
            Vi.addInitHook("addHandler", "doubleClickZoom", pn), Vi.mergeOptions({
                dragging: !0,
                inertia: !et,
                inertiaDeceleration: 3400,
                inertiaMaxSpeed: 1 / 0,
                easeLinearity: .2,
                worldCopyJump: !1,
                maxBoundsViscosity: 0
            });
            var mn = $i.extend({
                addHooks: function () {
                    if (!this._draggable) {
                        var t = this._map;
                        this._draggable = new oe(t._mapPane, t._container), this._draggable.on({
                            dragstart: this._onDragStart,
                            drag: this._onDrag,
                            dragend: this._onDragEnd
                        }, this), this._draggable.on("predrag", this._onPreDragLimit, this), t.options.worldCopyJump && (this._draggable.on("predrag", this._onPreDragWrap, this), t.on("zoomend", this._onZoomEnd, this), t.whenReady(this._onZoomEnd, this))
                    }
                    ai(this._map._container, "leaflet-grab leaflet-touch-drag"), this._draggable.enable(), this._positions = [], this._times = []
                }, removeHooks: function () {
                    hi(this._map._container, "leaflet-grab"), hi(this._map._container, "leaflet-touch-drag"), this._draggable.disable()
                }, moved: function () {
                    return this._draggable && this._draggable._moved
                }, moving: function () {
                    return this._draggable && this._draggable._moving
                }, _onDragStart: function () {
                    var t = this._map;
                    if (t._stop(), this._map.options.maxBounds && this._map.options.maxBoundsViscosity) {
                        var i = R(this._map.options.maxBounds);
                        this._offsetLimit = I(this._map.latLngToContainerPoint(i.getNorthWest()).multiplyBy(-1), this._map.latLngToContainerPoint(i.getSouthEast()).multiplyBy(-1).add(this._map.getSize())), this._viscosity = Math.min(1, Math.max(0, this._map.options.maxBoundsViscosity))
                    } else this._offsetLimit = null;
                    t.fire("movestart").fire("dragstart"), t.options.inertia && (this._positions = [], this._times = [])
                }, _onDrag: function (t) {
                    if (this._map.options.inertia) {
                        var i = this._lastTime = +new Date,
                            e = this._lastPos = this._draggable._absPos || this._draggable._newPos;
                        this._positions.push(e), this._times.push(i), this._prunePositions(i)
                    }
                    this._map.fire("move", t).fire("drag", t)
                }, _prunePositions: function (t) {
                    for (; this._positions.length > 1 && t - this._times[0] > 50;) this._positions.shift(), this._times.shift()
                }, _onZoomEnd: function () {
                    var t = this._map.getSize().divideBy(2), i = this._map.latLngToLayerPoint([0, 0]);
                    this._initialWorldOffset = i.subtract(t).x, this._worldWidth = this._map.getPixelWorldBounds().getSize().x
                }, _viscousLimit: function (t, i) {
                    return t - (t - i) * this._viscosity
                }, _onPreDragLimit: function () {
                    if (this._viscosity && this._offsetLimit) {
                        var t = this._draggable._newPos.subtract(this._draggable._startPos), i = this._offsetLimit;
                        t.x < i.min.x && (t.x = this._viscousLimit(t.x, i.min.x)), t.y < i.min.y && (t.y = this._viscousLimit(t.y, i.min.y)), t.x > i.max.x && (t.x = this._viscousLimit(t.x, i.max.x)), t.y > i.max.y && (t.y = this._viscousLimit(t.y, i.max.y)), this._draggable._newPos = this._draggable._startPos.add(t)
                    }
                }, _onPreDragWrap: function () {
                    var t = this._worldWidth, i = Math.round(t / 2), e = this._initialWorldOffset,
                        n = this._draggable._newPos.x, o = (n - i + e) % t + i - e, s = (n + i + e) % t - i - e,
                        r = Math.abs(o + e) < Math.abs(s + e) ? o : s;
                    this._draggable._absPos = this._draggable._newPos.clone(), this._draggable._newPos.x = r
                }, _onDragEnd: function (t) {
                    var i = this._map, e = i.options, n = !e.inertia || this._times.length < 2;
                    if (i.fire("dragend", t), n) i.fire("moveend"); else {
                        this._prunePositions(+new Date);
                        var o = this._lastPos.subtract(this._positions[0]), s = (this._lastTime - this._times[0]) / 1e3,
                            r = e.easeLinearity, a = o.multiplyBy(r / s), h = a.distanceTo([0, 0]),
                            u = Math.min(e.inertiaMaxSpeed, h), l = a.multiplyBy(u / h),
                            c = u / (e.inertiaDeceleration * r), _ = l.multiplyBy(-c / 2).round();
                        _.x || _.y ? (_ = i._limitOffset(_, i.options.maxBounds), T(function () {
                            i.panBy(_, {duration: c, easeLinearity: r, noMoveStart: !0, animate: !0})
                        })) : i.fire("moveend")
                    }
                }
            });
            Vi.addInitHook("addHandler", "dragging", mn), Vi.mergeOptions({keyboard: !0, keyboardPanDelta: 80});
            var fn = $i.extend({
                keyCodes: {
                    left: [37],
                    right: [39],
                    down: [40],
                    up: [38],
                    zoomIn: [187, 107, 61, 171],
                    zoomOut: [189, 109, 54, 173]
                }, initialize: function (t) {
                    this._map = t, this._setPanDelta(t.options.keyboardPanDelta), this._setZoomDelta(t.options.zoomDelta)
                }, addHooks: function () {
                    try {
                        var t = this._map._container;
                    t.tabIndex <= 0 && (t.tabIndex = "0"), bi(t, {
                        focus: this._onFocus,
                        blur: this._onBlur,
                        mousedown: this._onMouseDown
                    }, this), this._map.on({focus: this._addHooks, blur: this._removeHooks}, this)
                    }catch (e) {

                    }

                }, removeHooks: function () {
                    this._removeHooks(), Mi(this._map._container, {
                        focus: this._onFocus,
                        blur: this._onBlur,
                        mousedown: this._onMouseDown
                    }, this), this._map.off({focus: this._addHooks, blur: this._removeHooks}, this)
                }, _onMouseDown: function () {
                    if (!this._focused) {
                        var t = document.body, i = document.documentElement, e = t.scrollTop || i.scrollTop,
                            n = t.scrollLeft || i.scrollLeft;
                        this._map._container.focus(), window.scrollTo(n, e)
                    }
                }, _onFocus: function () {
                    this._focused = !0, this._map.fire("focus")
                }, _onBlur: function () {
                    this._focused = !1, this._map.fire("blur")
                }, _setPanDelta: function (t) {
                    var i, e, n = this._panKeys = {}, o = this.keyCodes;
                    for (i = 0, e = o.left.length; i < e; i++) n[o.left[i]] = [-1 * t, 0];
                    for (i = 0, e = o.right.length; i < e; i++) n[o.right[i]] = [t, 0];
                    for (i = 0, e = o.down.length; i < e; i++) n[o.down[i]] = [0, t];
                    for (i = 0, e = o.up.length; i < e; i++) n[o.up[i]] = [0, -1 * t]
                }, _setZoomDelta: function (t) {
                    var i, e, n = this._zoomKeys = {}, o = this.keyCodes;
                    for (i = 0, e = o.zoomIn.length; i < e; i++) n[o.zoomIn[i]] = t;
                    for (i = 0, e = o.zoomOut.length; i < e; i++) n[o.zoomOut[i]] = -t
                }, _addHooks: function () {
                    bi(document, "keydown", this._onKeyDown, this)
                }, _removeHooks: function () {
                    Mi(document, "keydown", this._onKeyDown, this)
                }, _onKeyDown: function (t) {
                    if (!(t.altKey || t.ctrlKey || t.metaKey)) {
                        var i, e = t.keyCode, n = this._map;
                        if (e in this._panKeys) n._panAnim && n._panAnim._inProgress || (i = this._panKeys[e], t.shiftKey && (i = B(i).multiplyBy(3)), n.panBy(i), n.options.maxBounds && n.panInsideBounds(n.options.maxBounds)); else if (e in this._zoomKeys) n.setZoom(n.getZoom() + (t.shiftKey ? 3 : 1) * this._zoomKeys[e]); else {
                            if (27 !== e || !n._popup || !n._popup.options.closeOnEscapeKey) return;
                            n.closePopup()
                        }
                        Ii(t)
                    }
                }
            });
            Vi.addInitHook("addHandler", "keyboard", fn), Vi.mergeOptions({
                scrollWheelZoom: !0,
                wheelDebounceTime: 40,
                wheelPxPerZoomLevel: 60
            });
            var gn = $i.extend({
                addHooks: function () {
                    bi(this._map._container, "wheel", this._onWheelScroll, this), this._delta = 0
                }, removeHooks: function () {
                    Mi(this._map._container, "wheel", this._onWheelScroll, this)
                }, _onWheelScroll: function (t) {
                    var i = Ni(t), e = this._map.options.wheelDebounceTime;
                    this._delta += i, this._lastMousePos = this._map.mouseEventToContainerPoint(t), this._startTime || (this._startTime = +new Date);
                    var o = Math.max(e - (+new Date - this._startTime), 0);
                    clearTimeout(this._timer), this._timer = setTimeout(n(this._performZoom, this), o), Ii(t)
                }, _performZoom: function () {
                    var t = this._map, i = t.getZoom(), e = this._map.options.zoomSnap || 0;
                    t._stop();
                    var n = this._delta / (4 * this._map.options.wheelPxPerZoomLevel),
                        o = 4 * Math.log(2 / (1 + Math.exp(-Math.abs(n)))) / Math.LN2, s = e ? Math.ceil(o / e) * e : o,
                        r = t._limitZoom(i + (this._delta > 0 ? s : -s)) - i;
                    this._delta = 0, this._startTime = null, r && ("center" === t.options.scrollWheelZoom ? t.setZoom(i + r) : t.setZoomAround(this._lastMousePos, i + r))
                }
            });
            Vi.addInitHook("addHandler", "scrollWheelZoom", gn), Vi.mergeOptions({tap: !0, tapTolerance: 15});
            var vn = $i.extend({
                addHooks: function () {
                    bi(this._map._container, "touchstart", this._onDown, this)
                }, removeHooks: function () {
                    Mi(this._map._container, "touchstart", this._onDown, this)
                }, _onDown: function (t) {
                    if (t.touches) {
                        if (Ai(t), this._fireClick = !0, t.touches.length > 1) return this._fireClick = !1, void clearTimeout(this._holdTimeout);
                        var i = t.touches[0], e = i.target;
                        this._startPos = this._newPos = new E(i.clientX, i.clientY), e.tagName && "a" === e.tagName.toLowerCase() && ai(e, "leaflet-active"), this._holdTimeout = setTimeout(n(function () {
                            this._isTapValid() && (this._fireClick = !1, this._onUp(), this._simulateEvent("contextmenu", i))
                        }, this), 1e3), this._simulateEvent("mousedown", i), bi(document, {
                            touchmove: this._onMove,
                            touchend: this._onUp
                        }, this)
                    }
                }, _onUp: function (t) {
                    if (clearTimeout(this._holdTimeout), Mi(document, {
                        touchmove: this._onMove,
                        touchend: this._onUp
                    }, this), this._fireClick && t && t.changedTouches) {
                        var i = t.changedTouches[0], e = i.target;
                        e && e.tagName && "a" === e.tagName.toLowerCase() && hi(e, "leaflet-active"), this._simulateEvent("mouseup", i), this._isTapValid() && this._simulateEvent("click", i)
                    }
                }, _isTapValid: function () {
                    return this._newPos.distanceTo(this._startPos) <= this._map.options.tapTolerance
                }, _onMove: function (t) {
                    var i = t.touches[0];
                    this._newPos = new E(i.clientX, i.clientY), this._simulateEvent("mousemove", i)
                }, _simulateEvent: function (t, i) {
                    var e = document.createEvent("MouseEvents");
                    e._simulated = !0, i.target._simulatedClick = !0, e.initMouseEvent(t, !0, !0, window, 1, i.screenX, i.screenY, i.clientX, i.clientY, !1, !1, !1, !1, 0, null), i.target.dispatchEvent(e)
                }
            });
            !wt || xt && !ht || Vi.addInitHook("addHandler", "tap", vn), Vi.mergeOptions({
                touchZoom: wt && !et,
                bounceAtZoomLimits: !0
            });
            var yn = $i.extend({
                addHooks: function () {
                    ai(this._map._container, "leaflet-touch-zoom"), bi(this._map._container, "touchstart", this._onTouchStart, this)
                }, removeHooks: function () {
                    hi(this._map._container, "leaflet-touch-zoom"), Mi(this._map._container, "touchstart", this._onTouchStart, this)
                }, _onTouchStart: function (t) {
                    var i = this._map;
                    if (t.touches && 2 === t.touches.length && !i._animatingZoom && !this._zooming) {
                        var e = i.mouseEventToContainerPoint(t.touches[0]),
                            n = i.mouseEventToContainerPoint(t.touches[1]);
                        this._centerPoint = i.getSize()._divideBy(2), this._startLatLng = i.containerPointToLatLng(this._centerPoint), "center" !== i.options.touchZoom && (this._pinchStartLatLng = i.containerPointToLatLng(e.add(n)._divideBy(2))), this._startDist = e.distanceTo(n), this._startZoom = i.getZoom(), this._moved = !1, this._zooming = !0, i._stop(), bi(document, "touchmove", this._onTouchMove, this), bi(document, "touchend", this._onTouchEnd, this), Ai(t)
                    }
                }, _onTouchMove: function (t) {
                    if (t.touches && 2 === t.touches.length && this._zooming) {
                        var i = this._map, e = i.mouseEventToContainerPoint(t.touches[0]),
                            o = i.mouseEventToContainerPoint(t.touches[1]), s = e.distanceTo(o) / this._startDist;
                        if (this._zoom = i.getScaleZoom(s, this._startZoom), !i.options.bounceAtZoomLimits && (this._zoom < i.getMinZoom() && s < 1 || this._zoom > i.getMaxZoom() && s > 1) && (this._zoom = i._limitZoom(this._zoom)), "center" === i.options.touchZoom) {
                            if (this._center = this._startLatLng, 1 === s) return
                        } else {
                            var r = e._add(o)._divideBy(2)._subtract(this._centerPoint);
                            if (1 === s && 0 === r.x && 0 === r.y) return;
                            this._center = i.unproject(i.project(this._pinchStartLatLng, this._zoom).subtract(r), this._zoom)
                        }
                        this._moved || (i._moveStart(!0, !1), this._moved = !0), M(this._animRequest);
                        var a = n(i._move, i, this._center, this._zoom, {pinch: !0, round: !1});
                        this._animRequest = T(a, this, !0), Ai(t)
                    }
                }, _onTouchEnd: function () {
                    this._moved && this._zooming ? (this._zooming = !1, M(this._animRequest), Mi(document, "touchmove", this._onTouchMove, this), Mi(document, "touchend", this._onTouchEnd, this), this._map.options.zoomAnimation ? this._map._animateZoom(this._center, this._map._limitZoom(this._zoom), !0, this._map.options.zoomSnap) : this._map._resetView(this._center, this._map._limitZoom(this._zoom))) : this._zooming = !1
                }
            });
            Vi.addInitHook("addHandler", "touchZoom", yn), Vi.BoxZoom = dn, Vi.DoubleClickZoom = pn, Vi.Drag = mn, Vi.Keyboard = fn, Vi.ScrollWheelZoom = gn, Vi.Tap = vn, Vi.TouchZoom = yn, t.version = "1.7.1", t.Control = qi, t.control = Gi, t.Browser = Zt, t.Evented = Z, t.Mixin = te, t.Util = z, t.Class = C, t.Handler = $i, t.extend = i, t.bind = n, t.stamp = s, t.setOptions = _, t.DomEvent = Fi, t.DomUtil = Li, t.PosAnimation = Ui, t.Draggable = oe, t.LineUtil = de, t.PolyUtil = me, t.Point = E, t.point = B, t.Bounds = A, t.bounds = I, t.Transformation = U, t.transformation = V, t.Projection = ve, t.LatLng = N, t.latLng = D, t.LatLngBounds = O, t.latLngBounds = R, t.CRS = W, t.GeoJSON = Ae, t.geoJSON = Ue, t.geoJson = Ve, t.Layer = Pe, t.LayerGroup = Le, t.layerGroup = function (t, i) {
                return new Le(t, i)
            }, t.FeatureGroup = be, t.featureGroup = function (t, i) {
                return new be(t, i)
            }, t.ImageOverlay = qe, t.imageOverlay = function (t, i, e) {
                return new qe(t, i, e)
            }, t.VideoOverlay = Ge, t.videoOverlay = function (t, i, e) {
                return new Ge(t, i, e)
            }, t.SVGOverlay = Ke, t.svgOverlay = function (t, i, e) {
                return new Ke(t, i, e)
            }, t.DivOverlay = Ye, t.Popup = Xe, t.popup = function (t, i) {
                return new Xe(t, i)
            }, t.Tooltip = Je, t.tooltip = function (t, i) {
                return new Je(t, i)
            }, t.Icon = Te, t.icon = function (t) {
                return new Te(t)
            }, t.DivIcon = $e, t.divIcon = function (t) {
                return new $e(t)
            }, t.Marker = Ce, t.marker = function (t, i) {
                return new Ce(t, i)
            }, t.TileLayer = tn, t.tileLayer = en, t.GridLayer = Qe, t.gridLayer = function (t) {
                return new Qe(t)
            }, t.SVG = ln, t.svg = cn, t.Renderer = on, t.Canvas = sn, t.canvas = rn, t.Path = Se, t.CircleMarker = Ze, t.circleMarker = function (t, i) {
                return new Ze(t, i)
            }, t.Circle = Ee, t.circle = function (t, i, e) {
                return new Ee(t, i, e)
            }, t.Polyline = ke, t.polyline = function (t, i) {
                return new ke(t, i)
            }, t.Polygon = Be, t.polygon = function (t, i) {
                return new Be(t, i)
            }, t.Rectangle = _n, t.rectangle = function (t, i) {
                return new _n(t, i)
            }, t.Map = Vi, t.map = function (t, i) {
                return new Vi(t, i)
            };
            var xn = window.L;
            t.noConflict = function () {
                return window.L = xn, this
            }, window.L = t
        });
    }, {}], "WMBG": [function (require, module, exports) {
        !function (t) {
            var n = {};

            function e(i) {
                if (n[i]) return n[i].exports;
                var a = n[i] = {i: i, l: !1, exports: {}};
                return t[i].call(a.exports, a, a.exports, e), a.l = !0, a.exports
            }

            e.m = t, e.c = n, e.d = function (t, n, i) {
                e.o(t, n) || Object.defineProperty(t, n, {enumerable: !0, get: i})
            }, e.r = function (t) {
                "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {value: "Module"}), Object.defineProperty(t, "__esModule", {value: !0})
            }, e.t = function (t, n) {
                if (1 & n && (t = e(t)), 8 & n) return t;
                if (4 & n && "object" == typeof t && t && t.__esModule) return t;
                var i = Object.create(null);
                if (e.r(i), Object.defineProperty(i, "default", {
                    enumerable: !0,
                    value: t
                }), 2 & n && "string" != typeof t) for (var a in t) e.d(i, a, function (n) {
                    return t[n]
                }.bind(null, a));
                return i
            }, e.n = function (t) {
                var n = t && t.__esModule ? function () {
                    return t.default
                } : function () {
                    return t
                };
                return e.d(n, "a", n), n
            }, e.o = function (t, n) {
                return Object.prototype.hasOwnProperty.call(t, n)
            }, e.p = "", e(e.s = 0)
        }([function (t, n) {
            L.Curve = L.Path.extend({
                options: {}, initialize: function (t, n) {
                    L.setOptions(this, n), this._setPath(t)
                }, setLatLngs: function (t) {
                    return this.setPath(t)
                }, getLatLngs: function () {
                    return this.getPath()
                }, _updateBounds: function () {
                    var t = this._clickTolerance(), n = new L.Point(t, t);
                    this._pxBounds = new L.Bounds([this._rawPxBounds.min.subtract(n), this._rawPxBounds.max.add(n)])
                }, getPath: function () {
                    return this._coords
                }, setPath: function (t) {
                    return this._setPath(t), this.redraw()
                }, getBounds: function () {
                    return this._bounds
                }, _setPath: function (t) {
                    this._coords = t, this._bounds = this._computeBounds()
                }, _computeBounds: function () {
                    for (var t, n, e, i = new L.LatLngBounds, a = 0; a < this._coords.length; a++) if ("string" == typeof (e = this._coords[a]) || e instanceof String) n = e; else if ("H" == n) i.extend([t.lat, e[0]]), t = new L.latLng(t.lat, e[0]); else if ("V" == n) i.extend([e[0], t.lng]), t = new L.latLng(e[0], t.lng); else if ("C" == n) {
                        var s = new L.latLng(e[0], e[1]);
                        e = this._coords[++a];
                        var o = new L.latLng(e[0], e[1]);
                        e = this._coords[++a];
                        var r = new L.latLng(e[0], e[1]);
                        i.extend(s), i.extend(o), i.extend(r), r.controlPoint1 = s, r.controlPoint2 = o, t = r
                    } else if ("S" == n) {
                        if (o = new L.latLng(e[0], e[1]), e = this._coords[++a], r = new L.latLng(e[0], e[1]), s = t, t.controlPoint2) {
                            var h = t.lat - t.controlPoint2.lat, c = t.lng - t.controlPoint2.lng;
                            s = new L.latLng(t.lat + h, t.lng + c)
                        }
                        i.extend(s), i.extend(o), i.extend(r), r.controlPoint1 = s, r.controlPoint2 = o, t = r
                    } else if ("Q" == n) {
                        var u = new L.latLng(e[0], e[1]);
                        e = this._coords[++a], r = new L.latLng(e[0], e[1]), i.extend(u), i.extend(r), r.controlPoint = u, t = r
                    } else "T" == n ? (r = new L.latLng(e[0], e[1]), u = t, t.controlPoint && (h = t.lat - t.controlPoint.lat, c = t.lng - t.controlPoint.lng, u = new L.latLng(t.lat + h, t.lng + c)), i.extend(u), i.extend(r), r.controlPoint = u, t = r) : (i.extend(e), t = new L.latLng(e[0], e[1]));
                    return i
                }, getCenter: function () {
                    return this._bounds.getCenter()
                }, _update: function () {
                    this._map && this._updatePath()
                }, _updatePath: function () {
                    this._usingCanvas ? this._updateCurveCanvas() : this._updateCurveSvg()
                }, _project: function () {
                    var t, n, e, i;
                    this._points = [];
                    for (var a = 0; a < this._coords.length; a++) if ("string" == typeof (t = this._coords[a]) || t instanceof String) this._points.push(t), e = t; else {
                        switch (t.length) {
                            case 2:
                                i = this._map.latLngToLayerPoint(t), n = t;
                                break;
                            case 1:
                                "H" == e ? (i = this._map.latLngToLayerPoint([n[0], t[0]]), n = [n[0], t[0]]) : (i = this._map.latLngToLayerPoint([t[0], n[1]]), n = [t[0], n[1]])
                        }
                        this._points.push(i)
                    }
                    if (this._bounds.isValid()) {
                        var s = this._map.latLngToLayerPoint(this._bounds.getNorthWest()),
                            o = this._map.latLngToLayerPoint(this._bounds.getSouthEast());
                        this._rawPxBounds = new L.Bounds(s, o), this._updateBounds()
                    }
                }, _curvePointsToPath: function (t) {
                    for (var n, e, i = "", a = 0; a < t.length; a++) if ("string" == typeof (n = t[a]) || n instanceof String) i += e = n; else switch (e) {
                        case"H":
                            i += n.x + " ";
                            break;
                        case"V":
                            i += n.y + " ";
                            break;
                        default:
                            i += n.x + "," + n.y + " "
                    }
                    return i || "M0 0"
                }, beforeAdd: function (t) {
                    L.Path.prototype.beforeAdd.call(this, t), this._usingCanvas = this._renderer instanceof L.Canvas, this._usingCanvas && (this._pathSvgElement = document.createElementNS("http://www.w3.org/2000/svg", "path"))
                }, onAdd: function (t) {
                    if (this._usingCanvas && (this._canvasSetDashArray = !this.options.dashArray), L.Path.prototype.onAdd.call(this, t), this._usingCanvas) this.options.animate && "object" == typeof TWEEN ? (this._normalizeCanvasAnimationOptions(), this._tweenedObject = {offset: this._pathSvgElement.getTotalLength()}, this._tween = new TWEEN.Tween(this._tweenedObject).to({offset: 0}, this.options.animate.duration).delay(this.options.animate.delay).repeat(this.options.animate.iterations - 1).onComplete(function (t) {
                        return function () {
                            t._canvasAnimating = !1
                        }
                    }(this)).start(), this._canvasAnimating = !0, this._animateCanvas()) : this._canvasAnimating = !1; else if (this.options.animate && this._path.animate) {
                        var n = this._svgSetDashArray();
                        this._path.animate([{strokeDashoffset: n}, {strokeDashoffset: 0}], this.options.animate)
                    }
                }, _updateCurveSvg: function () {
                    this._renderer._setPath(this, this._curvePointsToPath(this._points)), this.options.animate && this._svgSetDashArray()
                }, _svgSetDashArray: function () {
                    var t = this._path, n = t.getTotalLength();
                    return this.options.dashArray || (t.style.strokeDasharray = n + " " + n), n
                }, _containsPoint: function (t) {
                    return !!this._bounds.isValid() && this._bounds.contains(this._map.layerPointToLatLng(t))
                }, _normalizeCanvasAnimationOptions: function () {
                    var t = {delay: 0, duration: 0, iterations: 1};
                    "number" == typeof this.options.animate ? t.duration = this.options.animate : (this.options.animate.duration && (t.duration = this.options.animate.duration), this.options.animate.delay && (t.delay = this.options.animate.delay), this.options.animate.iterations && (t.iterations = this.options.animate.iterations)), this.options.animate = t
                }, _updateCurveCanvas: function () {
                    var t = this._curvePointsToPath(this._points);
                    this._pathSvgElement.setAttribute("d", t), this.options.animate && "object" == typeof TWEEN && this._canvasSetDashArray && (this.options.dashArray = this._pathSvgElement.getTotalLength() + "", this._renderer._updateDashArray(this)), this._curveFillStroke(new Path2D(t), this._renderer._ctx)
                }, _animateCanvas: function () {
                    TWEEN.update(), this._renderer._updatePaths(), this._canvasAnimating && (this._animationFrameId = L.Util.requestAnimFrame(this._animateCanvas, this))
                }, _curveFillStroke: function (t, n) {
                    n.lineDashOffset = this._canvasAnimating ? this._tweenedObject.offset : 0;
                    var e = this.options;
                    e.fill && (n.globalAlpha = e.fillOpacity, n.fillStyle = e.fillColor || e.color, n.fill(t, e.fillRule || "evenodd")), e.stroke && 0 !== e.weight && (n.setLineDash && n.setLineDash(this.options && this.options._dashArray || []), n.globalAlpha = e.opacity, n.lineWidth = e.weight, n.strokeStyle = e.color, n.lineCap = e.lineCap, n.lineJoin = e.lineJoin, n.stroke(t))
                }, trace: function (t) {
                    if (void 0 === this._map || null === this._map) return [];
                    var n, e, i, a, s, o, r;
                    t = t.filter(function (t) {
                        return t >= 0 && t <= 1
                    });
                    for (var h = [], c = 0; c < this._points.length; c++) if ("string" == typeof (n = this._points[c]) || n instanceof String) "Z" == (e = n) && (h = h.concat(this._linearTrace(t, a, i))); else switch (e) {
                        case"M":
                            i = n, a = n;
                            break;
                        case"L":
                        case"H":
                        case"V":
                            h = h.concat(this._linearTrace(t, a, n)), a = n;
                            break;
                        case"C":
                            s = n, o = this._points[++c], r = this._points[++c], h = h.concat(this._cubicTrace(t, a, s, o, r)), a = r;
                            break;
                        case"S":
                            s = this._reflectPoint(o, a), o = n, r = this._points[++c], h = h.concat(this._cubicTrace(t, a, s, o, r)), a = r;
                            break;
                        case"Q":
                            s = n, o = this._points[++c], h = h.concat(this._quadraticTrace(t, a, s, o)), a = o;
                            break;
                        case"T":
                            s = this._reflectPoint(s, a), o = n, h = h.concat(this._quadraticTrace(t, a, s, o)), a = o
                    }
                    return h
                }, _linearTrace: function (t, n, e) {
                    return t.map(t => {
                        var i = this._singleLinearTrace(t, n.x, e.x), a = this._singleLinearTrace(t, n.y, e.y);
                        return this._map.layerPointToLatLng([i, a])
                    })
                }, _quadraticTrace: function (t, n, e, i) {
                    return t.map(t => {
                        var a = this._singleQuadraticTrace(t, n.x, e.x, i.x),
                            s = this._singleQuadraticTrace(t, n.y, e.y, i.y);
                        return this._map.layerPointToLatLng([a, s])
                    })
                }, _cubicTrace: function (t, n, e, i, a) {
                    return t.map(t => {
                        var s = this._singleCubicTrace(t, n.x, e.x, i.x, a.x),
                            o = this._singleCubicTrace(t, n.y, e.y, i.y, a.y);
                        return this._map.layerPointToLatLng([s, o])
                    })
                }, _singleLinearTrace: function (t, n, e) {
                    return n + t * (e - n)
                }, _singleQuadraticTrace: function (t, n, e, i) {
                    var a = 1 - t;
                    return Math.pow(a, 2) * n + 2 * a * t * e + Math.pow(t, 2) * i
                }, _singleCubicTrace: function (t, n, e, i, a) {
                    var s = 1 - t;
                    return Math.pow(s, 3) * n + 3 * Math.pow(s, 2) * t * e + 3 * s * Math.pow(t, 2) * i + Math.pow(t, 3) * a
                }, _reflectPoint: function (t, n) {
                    return x = n.x + (n.x - t.x), y = n.y + (n.y - t.y), L.point(x, y)
                }
            }), L.curve = function (t, n) {
                return new L.Curve(t, n)
            }
        }]);
    }, {}], "Tnu0": [function (require, module, exports) {

    }, {}], "UnXq": [function (require, module, exports) {
        "use strict";
        var r = this && this.__assign || function () {
            return (r = Object.assign || function (r) {
                for (var t, e = 1, o = arguments.length; e < o; e++) for (var i in t = arguments[e]) Object.prototype.hasOwnProperty.call(t, i) && (r[i] = t[i]);
                return r
            }).apply(this, arguments)
        }, t = this && this.__createBinding || (Object.create ? function (r, t, e, o) {
            void 0 === o && (o = e), Object.defineProperty(r, o, {
                enumerable: !0, get: function () {
                    return t[e]
                }
            })
        } : function (r, t, e, o) {
            void 0 === o && (o = e), r[o] = t[e]
        }), e = this && this.__setModuleDefault || (Object.create ? function (r, t) {
            Object.defineProperty(r, "default", {enumerable: !0, value: t})
        } : function (r, t) {
            r.default = t
        }), o = this && this.__importStar || function (r) {
            if (r && r.__esModule) return r;
            var o = {};
            if (null != r) for (var i in r) "default" !== i && Object.prototype.hasOwnProperty.call(r, i) && t(o, r, i);
            return e(o, r), o
        }, i = this && this.__rest || function (r, t) {
            var e = {};
            for (var o in r) Object.prototype.hasOwnProperty.call(r, o) && t.indexOf(o) < 0 && (e[o] = r[o]);
            if (null != r && "function" == typeof Object.getOwnPropertySymbols) {
                var i = 0;
                for (o = Object.getOwnPropertySymbols(r); i < o.length; i++) t.indexOf(o[i]) < 0 && Object.prototype.propertyIsEnumerable.call(r, o[i]) && (e[o[i]] = r[o[i]])
            }
            return e
        };
        Object.defineProperty(exports, "__esModule", {value: !0}), exports.CoordSet = void 0;
        var n = o(require("leaflet")), a = {drawVertices: !0, fill: !0, weight: 10, color: "rgba(0,0,0,0.2)"},
            l = function () {
                function t(r) {
                    this.coords = r
                }

                return t.prototype.shift = function (r) {
                    var e = r.up, o = r.down, i = r.left, a = r.right;
                    return new t(this.coords.map(function (r) {
                        var t = r.lat, l = r.lng;
                        return e && (t += e), o && (t -= o), i && (l -= i), a && (l += a), n.latLng({lat: t, lng: l})
                    }))
                }, t.prototype.asPolyline = function (t) {
                    void 0 === t && (t = a);
                    var e = r(r({}, a), t), o = e.drawVertices, l = (e.fill, i(e, ["drawVertices", "fill"]));
                    if (o) {
                        var c = n.layerGroup();
                        return n.polyline(this.coords, r(r({}, e), {
                            interactive: !1,
                            fill: !1
                        })).addTo(c), this.coords.forEach(function (r, t) {
                            n.circleMarker(r, {radius: 5, color: "rgba(0,0,0,0.5)", interactive: !1}).addTo(c)
                        }), c
                    }
                    return n.polyline(this.coords, r(r({}, a), l))
                }, t.prototype.asPolygon = function (t) {
                    void 0 === t && (t = a);
                    var e = t.drawVertices, o = (t.fill, i(t, ["drawVertices", "fill"]));
                    if (e) {
                        var l = n.layerGroup();
                        return n.polygon(this.coords, r(r({}, o), {interactive: !1})).addTo(l), this.coords.forEach(function (r, t) {
                            n.circleMarker(r, {radius: 5, color: "rgba(0,0,0,0.5)", interactive: !1}).addTo(l)
                        }), l
                    }
                    return n.polygon(this.coords, o)
                }, t
            }();
        exports.CoordSet = l;
    }, {"leaflet": "f3z0"}], "eKDL": [function (require, module, exports) {
        "use strict";
        var e = this && this.__createBinding || (Object.create ? function (e, t, r, n) {
            void 0 === n && (n = r), Object.defineProperty(e, n, {
                enumerable: !0, get: function () {
                    return t[r]
                }
            })
        } : function (e, t, r, n) {
            void 0 === n && (n = r), e[n] = t[r]
        }), t = this && this.__setModuleDefault || (Object.create ? function (e, t) {
            Object.defineProperty(e, "default", {enumerable: !0, value: t})
        } : function (e, t) {
            e.default = t
        }), r = this && this.__importStar || function (r) {
            if (r && r.__esModule) return r;
            var n = {};
            if (null != r) for (var o in r) "default" !== o && Object.prototype.hasOwnProperty.call(r, o) && e(n, r, o);
            return t(n, r), n
        };
        Object.defineProperty(exports, "__esModule", {value: !0}), exports.shape2 = exports.shape3 = exports.shape1 = exports.TILE_LAYER_URL = void 0;
        var n = r(require("leaflet")), o = require("./utils");
        exports.TILE_LAYER_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}", exports.shape1 = new o.CoordSet([[-5.9765625, 2.9540126939036564], [-6.15234375, 2.591888984149953], [-5.833740234375, 2.4052990502867853], [-5.570068359375, 2.482133403730576], [-5.2294921875, 2.4492049339511506], [-4.954833984374999, 2.1308562777325313], [-4.32861328125, 2.054003264372146], [-3.8891601562499996, 2.28455066023697], [-4.04296875, 2.756504385543263], [-4.449462890625, 3.052753821574483], [-4.888916015625, 3.1843944923387464], [-5.548095703125, 3.1514858749293237], [-5.9765625, 2.9540126939036564]].map(function (e) {
            return n.latLng(e.reverse())
        }));
        var s = new o.CoordSet([[-6.5765625, 2.5540126939036565], [-6.15234375, 2.591888984149953], [-5.833740234375, 2.4052990502867853], [-5.570068359375, 2.482133403730576], [-5.2294921875, 2.4492049339511506], [-4.954833984374999, 2.1308562777325313], [-4.32861328125, 2.054003264372146], [-3.8891601562499996, 2.28455066023697], [-4.04296875, 2.756504385543263], [-4.449462890625, 3.052753821574483], [-4.888916015625, 3.1843944923387464]].map(function (e) {
            return n.latLng(e.reverse())
        }));
        exports.shape3 = new o.CoordSet([[-8, 3], [-9, 2.4], [-7.5, 1.7], [-9.5, .7]].map(function (e) {
            return n.latLng(e.reverse())
        })), exports.shape2 = s.shift({down: 1.5});
    }, {"leaflet": "f3z0", "./utils": "UnXq"}], "fUdq": [function (require, module, exports) {
        "use strict";
        var t = this && this.__extends || function () {
            var t = function (e, o) {
                return (t = Object.setPrototypeOf || {__proto__: []} instanceof Array && function (t, e) {
                    t.__proto__ = e
                } || function (t, e) {
                    for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && (t[o] = e[o])
                })(e, o)
            };
            return function (e, o) {
                if ("function" != typeof o && null !== o) throw new TypeError("Class extends value " + String(o) + " is not a constructor or null");

                function n() {
                    this.constructor = e
                }

                t(e, o), e.prototype = null === o ? Object.create(o) : (n.prototype = o.prototype, new n)
            }
        }(), e = this && this.__assign || function () {
            return (e = Object.assign || function (t) {
                for (var e, o = 1, n = arguments.length; o < n; o++) for (var r in e = arguments[o]) Object.prototype.hasOwnProperty.call(e, r) && (t[r] = e[r]);
                return t
            }).apply(this, arguments)
        }, o = this && this.__spreadArray || function (t, e, o) {
            if (o || 2 === arguments.length) for (var n, r = 0, i = e.length; r < i; r++) !n && r in e || (n || (n = Array.prototype.slice.call(e, 0, r)), n[r] = e[r]);
            return t.concat(n || Array.prototype.slice.call(e))
        }, n = this && this.__importDefault || function (t) {
            return t && t.__esModule ? t : {default: t}
        };
        Object.defineProperty(exports, "__esModule", {value: !0}), exports.spline = exports.Spline = void 0;
        var r = n(require("leaflet"));
        require("@elfalem/leaflet-curve");
        var i = function (t, e) {
            var o = e.x - t.x, n = e.y - t.y;
            return {length: Math.sqrt(Math.pow(o, 2) + Math.pow(n, 2)), angle: Math.atan2(n, o)}
        }, u = function (t, e, o, n, u, s) {
            var p = n || o, h = u || o, c = e.latLngToLayerPoint(r.default.latLng(o)),
                a = e.latLngToLayerPoint(r.default.latLng(p)), l = e.latLngToLayerPoint(r.default.latLng(h)),
                f = i(a, l), v = f.length, _ = f.angle;
            _ += s ? Math.PI : 0, v *= t;
            var y = c.x + Math.cos(_) * v, g = c.y + Math.sin(_) * v, d = e.layerPointToLatLng([y, g]);
            return [d.lat, d.lng]
        }, s = function (n) {
            function i(t, o) {
                var i, u = n.call(this, t, o) || this;
                return u._points = [], u._curve = new r.default.Curve([], e({}, o)), u._smoothing = null !== (i = o.smoothing) && void 0 !== i ? i : .15, u._transformPoints(t), u
            }

            return t(i, n), i.prototype._transformPoints = function (t) {
                Array.isArray(t[0]) && 2 === t[0].length ? this._points = t : t[0].lat && (this._points = t.map(function (t) {
                    return [t.lat, t.lng]
                }))
            }, i.prototype.drawBezier = function () {
                for (var t = o([], this._points, !0), n = o([], t[0], !0), i = t.length, s = t[0][0] === t[i - 1][0] && t[0][1] === t[i - 1][1], p = [], h = 0; h < i - 1; h++) p.push(u(this._smoothing, this._map, t[h], t[h + 1], t[h - 1])), p.push(u(this._smoothing, this._map, t[h], t[h - 1], t[h + 1]));
                if (s) {
                    var c = p.shift();
                    p.push(c), p[0] = u(this._smoothing, this._map, t[i - 1], t[i - 2], t[1]), p[p.length - 1] = u(this._smoothing, this._map, t[i - 1], t[1], t[i - 2])
                } else p.shift(), p.push(u(this._smoothing, this._map, t[i - 1], void 0, t[i - 2]));
                var a = ["M", n], l = (t = o([], this._points, !0)).shift();
                for (a.push.apply(a, ["L", l]); t.length > 0;) {
                    var f = p.shift(), v = p.shift(), _ = t.shift();
                    a.push.apply(a, ["C", f, v, _])
                }
                return s && a.push("Z"), this._curve ? this._curve.setPath(a) : this._curve = r.default.curve(a, e({}, this.options)), this._curve
            }, i.prototype.update = function () {
                this.drawBezier()
            }, i.prototype.onAdd = function (t) {
                var e = this;
                return this.drawBezier(), this._curve.addTo(t), t.on("zoomend", function () {
                    e.update()
                }), this
            }, i.prototype.onRemove = function (t) {
                var e = this;
                return t.off("zoomend", function () {
                    e.update()
                }), this._curve.remove(), this
            }, i.prototype.on = function (t, e, o) {
                return this._curve.on(t, e, o), this
            }, i.prototype.off = function (t, e, o) {
                return this._curve.off(t, e, o), this
            }, i.prototype.once = function (t, e, o) {
                return this._curve.once(t, e, o), this
            }, i.prototype.fire = function (t, e, o) {
                return this._curve.once(t, e, o), this
            }, i.prototype.listens = function (t) {
                return this._curve.listens(t)
            }, i.prototype.addEventParent = function (t) {
                return this._curve.addEventParent(t), this
            }, i.prototype.removeEventParent = function (t) {
                return this._curve.removeEventParent(t), this
            }, i.prototype.addEventListener = function (t, e, o) {
                return this._curve.addEventListener(t, e, o), this
            }, i.prototype.removeEventListener = function (t, e, o) {
                return this._curve.removeEventListener(t, e, o), this
            }, i.prototype.clearAllEventListeners = function () {
                return this._curve.clearAllEventListeners(), this
            }, i.prototype.fireEvent = function (t, e, o) {
                return this._curve.fireEvent(t, e, o), this
            }, i.prototype.hasEventListeners = function (t) {
                return this._curve.hasEventListeners(t)
            }, i.prototype.remove = function () {
                return this._curve.remove(), this
            }, i.prototype.removeFrom = function (t) {
                return this._curve.removeFrom(t), this
            }, i.prototype.getPane = function (t) {
                return this._curve.getPane(t)
            }, i.prototype.bindPopup = function (t, e) {
                return console.log(e), this._curve.bindPopup(t, e), this
            }, i.prototype.unbindPopup = function () {
                return this._curve.unbindPopup(), this
            }, i.prototype.openPopup = function (t) {
                return this._curve.openPopup(t), this
            }, i.prototype.closePopup = function () {
                return this._curve.closePopup(), this
            }, i.prototype.togglePopup = function () {
                return this._curve.togglePopup(), this
            }, i.prototype.isPopupOpen = function () {
                return this._curve.isPopupOpen()
            }, i.prototype.setPopupContent = function (t) {
                return this._curve.setPopupContent(t), this
            }, i.prototype.getPopup = function () {
                return this._curve.getPopup()
            }, i.prototype.bindTooltip = function (t, e) {
                return this._curve.bindTooltip(t, e), this
            }, i.prototype.unbindTooltip = function () {
                return this._curve.unbindTooltip(), this
            }, i.prototype.openTooltip = function (t) {
                return this._curve.openTooltip(t), this
            }, i.prototype.closeTooltip = function () {
                return this._curve.closeTooltip(), this
            }, i.prototype.toggleTooltip = function () {
                return this._curve.toggleTooltip(), this
            }, i.prototype.isTooltipOpen = function () {
                return this._curve.isTooltipOpen()
            }, i.prototype.setTooltipContent = function (t) {
                return this._curve.setTooltipContent(t), this
            }, i.prototype.getTooltip = function () {
                return this._curve.getTooltip()
            }, i.prototype.redraw = function () {
                return this._curve.redraw(), this
            }, i.prototype.setStyle = function (t) {
                return r.default.Util.setOptions(this, t), this._curve.setStyle(t), this
            }, i.prototype.bringToFront = function () {
                return this._curve.bringToFront(), this
            }, i.prototype.bringToBack = function () {
                return this._curve.bringToBack(), this
            }, i.prototype.getElement = function () {
                return this._curve.getElement()
            }, i.prototype.setLatLngs = function (t) {
                return this._transformPoints(t), this.drawBezier(), this
            }, i.prototype.trace = function (t) {
                return this._curve.trace(t)
            }, i
        }(r.default.Polyline);

        function p(t, e) {
            return void 0 === e && (e = {}), new s(t, e)
        }

        exports.Spline = s, exports.spline = p, r.default.Spline = s, r.default.spline = p;
    }, {"leaflet": "f3z0", "@elfalem/leaflet-curve": "WMBG"}], "QCba": [function (require, module, exports) {
        try {
            "use strict";
        var e = this && this.__importDefault || function (e) {
            return e && e.__esModule ? e : {default: e}
        };
        Object.defineProperty(exports, "__esModule", {value: !0}), exports.map = void 0, require("leaflet/dist/leaflet.css");
        var o = e(require("leaflet"));
        require("@elfalem/leaflet-curve"), require("./styles.css");
        var l = require("./constants");
        require("../src"), exports.map = o.default.map("map", {
            center: [2, -6.6],
            zoom: 8
        }), exports.map.createPane("splines"), exports.map.getPane("splines").style.zIndex = "650", o.default.tileLayer(l.TILE_LAYER_URL).addTo(exports.map);
        var n = l.shape1.asPolyline(), s = l.shape2.asPolyline(), p = l.shape3.asPolyline(),
            a = o.default.layerGroup([n, s, p]).addTo(exports.map), t = o.default.spline(l.shape1.coords, {
                fill: !0,
                color: "yellow",
                pane: "splines"
            }).bindPopup('<pre><code>\nL.spline(coords, {\n  fill: true,\n  color: "yellow"\n})\n</code></pre>', {minWidth: 200}).addTo(exports.map),
            r = o.default.spline(l.shape2.coords, {
                color: "yellow",
                pane: "splines"
            }).bindPopup('<pre><code>L.spline(coords, { color: "yellow" })</code></pre>', {minWidth: 300}).addTo(exports.map),
            i = o.default.spline(l.shape3.coords, {
                color: "yellow",
                pane: "splines"
            }).bindPopup('<pre><code>\n  L.spline(coords, { \n    color: "yellow",\n    smoothing: <span id="smoothing-example">0.15</span>\n  })\n  </code></pre>\n  <h4>Adjust the smoothing:</h4>\n  <input id="smoothing-input" type="number" value="0.15" min="0" max="1" step="0.01" onchange="applySmoothing()">', {minWidth: 300}).addTo(exports.map);

        function d() {
            var e, o = document.getElementById("smoothing-input").value;
            null === (e = document.getElementById("smoothing-example")) || void 0 === e || (e.innerHTML = o), i._smoothing = o, i.drawBezier()
        }

        window.applySmoothing = d, o.default.control.layers(void 0, {"Original Polygons": a}, {collapsed: !1}).addTo(exports.map);
        }catch (e) {

        }

    }, {
        "leaflet/dist/leaflet.css": "BWvR",
        "leaflet": "f3z0",
        "@elfalem/leaflet-curve": "WMBG",
        "./styles.css": "Tnu0",
        "./constants": "eKDL",
        "../src": "fUdq"
    }]
}, {}, ["QCba"], null)
//# sourceMappingURL=/leaflet-spline/example.c5858ccf.js.map