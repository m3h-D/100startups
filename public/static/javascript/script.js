// ! function (e, t) { "function" == typeof define && define.amd ? define(["exports"], t) : "object" == typeof exports && "string" != typeof exports.nodeName ? t(exports) : t(e.commonJsStrict = {}) }(this, function (e) {
//     "function" != typeof Promise && function (e) {
//         function t(e, t) { return function () { e.apply(t, arguments) } }

//         function i(e) {
//             if ("object" != typeof this) throw new TypeError("Promises must be constructed via new"); if ("function" != typeof e) throw new TypeError("not a function");
//             this._state = null, this._value = null, this._deferreds = [], s(e, t(o, this), t(r, this))
//         }

//         function n(e) {
//             var t = this; return null === this._state ? void this._deferreds.push(e) : void h(function () {
//                 var i = t._state ? e.onFulfilled : e.onRejected; if (null !== i) {
//                     var n; try { n = i(t._value) } catch (t) { return void e.reject(t) }
//                     e.resolve(n)
//                 } else (t._state ? e.resolve : e.reject)(t._value)
//             })
//         }

//         function o(e) {
//             try {
//                 if (e === this) throw new TypeError("A promise cannot be resolved with itself."); if (e && ("object" == typeof e || "function" == typeof e)) { var i = e.then; if ("function" == typeof i) return void s(t(i, e), t(o, this), t(r, this)) }
//                 this._state = !0, this._value = e, a.call(this)
//             } catch (e) { r.call(this, e) }
//         }

//         function r(e) { this._state = !1, this._value = e, a.call(this) }

//         function a() {
//             for (var e = 0, t = this._deferreds.length; t > e; e++) n.call(this, this._deferreds[e]);
//             this._deferreds = null
//         }

//         function s(e, t, i) {
//             var n = !1; try { e(function (e) { n || (n = !0, t(e)) }, function (e) { n || (n = !0, i(e)) }) } catch (e) {
//                 if (n) return;
//                 n = !0, i(e)
//             }
//         } var l = setTimeout,
//             h = "function" == typeof setImmediate && setImmediate || function (e) { l(e, 1) },
//             u = Array.isArray || function (e) { return "[object Array]" === Object.prototype.toString.call(e) };
//         i.prototype.catch = function (e) { return this.then(null, e) }, i.prototype.then = function (e, t) { var o = this; return new i(function (i, r) { n.call(o, new function (e, t, i, n) { this.onFulfilled = "function" == typeof e ? e : null, this.onRejected = "function" == typeof t ? t : null, this.resolve = i, this.reject = n }(e, t, i, r)) }) }, i.all = function () {
//             var e = Array.prototype.slice.call(1 === arguments.length && u(arguments[0]) ? arguments[0] : arguments); return new i(function (t, i) {
//                 function n(r, a) {
//                     try {
//                         if (a && ("object" == typeof a || "function" == typeof a)) { var s = a.then; if ("function" == typeof s) return void s.call(a, function (e) { n(r, e) }, i) }
//                         e[r] = a, 0 == --o && t(e)
//                     } catch (e) { i(e) }
//                 } if (0 === e.length) return t([]); for (var o = e.length, r = 0; r < e.length; r++) n(r, e[r])
//             })
//         }, i.resolve = function (e) { return e && "object" == typeof e && e.constructor === i ? e : new i(function (t) { t(e) }) }, i.reject = function (e) { return new i(function (t, i) { i(e) }) }, i.race = function (e) { return new i(function (t, i) { for (var n = 0, o = e.length; o > n; n++) e[n].then(t, i) }) }, i._setImmediateFn = function (e) { h = e }, "undefined" != typeof module && module.exports ? module.exports = i : e.Promise || (e.Promise = i)
//     }(this), "function" != typeof window.CustomEvent && function () {
//         function e(e, t) { t = t || { bubbles: !1, cancelable: !1, detail: void 0 }; var i = document.createEvent("CustomEvent"); return i.initCustomEvent(e, t.bubbles, t.cancelable, t.detail), i }
//         e.prototype = window.Event.prototype, window.CustomEvent = e
//     }(), HTMLCanvasElement.prototype.toBlob || Object.defineProperty(HTMLCanvasElement.prototype, "toBlob", {
//         value: function (e, t, i) {
//             for (var n = atob(this.toDataURL(t, i).split(",")[1]), o = n.length, r = new Uint8Array(o), a = 0; a < o; a++) r[a] = n.charCodeAt(a);
//             e(new Blob([r], { type: t || "image/png" }))
//         }
//     }); var t, i, n, o = ["Webkit", "Moz", "ms"],
//         r = document.createElement("div").style,
//         a = [1, 8, 3, 6],
//         s = [2, 7, 4, 5];

//     function l(e) {
//         if (e in r) return e; for (var t = e[0].toUpperCase() + e.slice(1), i = o.length; i--;)
//             if ((e = o[i] + t) in r) return e
//     }

//     function h(e, t) { e = e || {}; for (var i in t) t[i] && t[i].constructor && t[i].constructor === Object ? (e[i] = e[i] || {}, h(e[i], t[i])) : e[i] = t[i]; return e }

//     function u(e) { return h({}, e) }

//     function c(e) {
//         if ("createEvent" in document) {
//             var t = document.createEvent("HTMLEvents");
//             t.initEvent("change", !1, !0), e.dispatchEvent(t)
//         } else e.fireEvent("onchange")
//     }

//     function p(e, t, i) {
//         if ("string" == typeof t) {
//             var n = t;
//             (t = {})[n] = i
//         } for (var o in t) e.style[o] = t[o]
//     }

//     function d(e, t) { e.classList ? e.classList.add(t) : e.className += " " + t }

//     function m(e, t) { for (var i in t) e.setAttribute(i, t[i]) }

//     function f(e) { return parseInt(e, 10) }

//     function v(e, t) {
//         var i = e.naturalWidth,
//             n = e.naturalHeight,
//             o = t || b(e); if (o && o >= 5) {
//                 var r = i;
//                 i = n, n = r
//             } return { width: i, height: n }
//     }
//     i = l("transform"), t = l("transformOrigin"), n = l("userSelect"); var g = { translate3d: { suffix: ", 0px" }, translate: { suffix: "" } },
//         w = function (e, t, i) { this.x = parseFloat(e), this.y = parseFloat(t), this.scale = parseFloat(i) };
//     w.parse = function (e) { return e.style ? w.parse(e.style[i]) : e.indexOf("matrix") > -1 || e.indexOf("none") > -1 ? w.fromMatrix(e) : w.fromString(e) }, w.fromMatrix = function (e) { var t = e.substring(7).split(","); return t.length && "none" !== e || (t = [1, 0, 0, 1, 0, 0]), new w(f(t[4]), f(t[5]), parseFloat(t[0])) }, w.fromString = function (e) {
//         var t = e.split(") "),
//             i = t[0].substring(q.globals.translate.length + 1).split(","),
//             n = t.length > 1 ? t[1].substring(6) : 1,
//             o = i.length > 1 ? i[0] : 0,
//             r = i.length > 1 ? i[1] : 0; return new w(o, r, n)
//     }, w.prototype.toString = function () { var e = g[q.globals.translate].suffix || ""; return q.globals.translate + "(" + this.x + "px, " + this.y + "px" + e + ") scale(" + this.scale + ")" }; var y = function (e) {
//         if (!e || !e.style[t]) return this.x = 0, void (this.y = 0); var i = e.style[t].split(" ");
//         this.x = parseFloat(i[0]), this.y = parseFloat(i[1])
//     };

//     function b(e) { return e.exifdata ? e.exifdata.Orientation : 1 }

//     function x(e, t, i) {
//         var n = t.width,
//             o = t.height,
//             r = e.getContext("2d"); switch (e.width = t.width, e.height = t.height, r.save(), i) {
//                 case 2:
//                     r.translate(n, 0), r.scale(-1, 1); break;
//                 case 3:
//                     r.translate(n, o), r.rotate(180 * Math.PI / 180); break;
//                 case 4:
//                     r.translate(0, o), r.scale(1, -1); break;
//                 case 5:
//                     e.width = o, e.height = n, r.rotate(90 * Math.PI / 180), r.scale(1, -1); break;
//                 case 6:
//                     e.width = o, e.height = n, r.rotate(90 * Math.PI / 180), r.translate(0, -o); break;
//                 case 7:
//                     e.width = o, e.height = n, r.rotate(-90 * Math.PI / 180), r.translate(-n, o), r.scale(1, -1); break;
//                 case 8:
//                     e.width = o, e.height = n, r.translate(0, n), r.rotate(-90 * Math.PI / 180)
//             }
//         r.drawImage(t, 0, 0, n, o), r.restore()
//     }

//     function C() {
//         var e, t, o, r, a, s = this.options.viewport.type ? "cr-vp-" + this.options.viewport.type : null;
//         this.options.useCanvas = this.options.enableOrientation || E.call(this), this.data = {}, this.elements = {}, e = this.elements.boundary = document.createElement("div"), t = this.elements.viewport = document.createElement("div"), this.elements.img = document.createElement("img"), o = this.elements.overlay = document.createElement("div"), this.options.useCanvas ? (this.elements.canvas = document.createElement("canvas"), this.elements.preview = this.elements.canvas) : this.elements.preview = this.elements.img, d(e, "cr-boundary"), e.setAttribute("aria-dropeffect", "none"), r = this.options.boundary.width, a = this.options.boundary.height, p(e, { width: r + (isNaN(r) ? "" : "px"), height: a + (isNaN(a) ? "" : "px") }), d(t, "cr-viewport"), s && d(t, s), p(t, { width: this.options.viewport.width + "px", height: this.options.viewport.height + "px" }), t.setAttribute("tabindex", 0), d(this.elements.preview, "cr-image"), m(this.elements.preview, { alt: "preview", "aria-grabbed": "false" }), d(o, "cr-overlay"), this.element.appendChild(e), e.appendChild(this.elements.preview), e.appendChild(t), e.appendChild(o), d(this.element, "croppie-container"), this.options.customClass && d(this.element, this.options.customClass),
//             function () {
//                 var e, t, o, r, a, s = this,
//                     l = !1;

//                 function h(e, t) {
//                     var i = s.elements.preview.getBoundingClientRect(),
//                         n = a.y + t,
//                         o = a.x + e;
//                     s.options.enforceBoundary ? (r.top > i.top + t && r.bottom < i.bottom + t && (a.y = n), r.left > i.left + e && r.right < i.right + e && (a.x = o)) : (a.y = n, a.x = o)
//                 }

//                 function u(e) { s.elements.preview.setAttribute("aria-grabbed", e), s.elements.boundary.setAttribute("aria-dropeffect", e ? "move" : "none") }

//                 function d(i) {
//                     if ((void 0 === i.button || 0 === i.button) && (i.preventDefault(), !l)) {
//                         if (l = !0, e = i.pageX, t = i.pageY, i.touches) {
//                             var o = i.touches[0];
//                             e = o.pageX, t = o.pageY
//                         }
//                         u(l), a = w.parse(s.elements.preview), window.addEventListener("mousemove", m), window.addEventListener("touchmove", m), window.addEventListener("mouseup", f), window.addEventListener("touchend", f), document.body.style[n] = "none", r = s.elements.viewport.getBoundingClientRect()
//                     }
//                 }

//                 function m(n) {
//                     n.preventDefault(); var r = n.pageX,
//                         l = n.pageY; if (n.touches) {
//                             var u = n.touches[0];
//                             r = u.pageX, l = u.pageY
//                         } var d = r - e,
//                             m = l - t,
//                             f = {}; if ("touchmove" === n.type && n.touches.length > 1) {
//                                 var v = n.touches[0],
//                                     g = n.touches[1],
//                                     w = Math.sqrt((v.pageX - g.pageX) * (v.pageX - g.pageX) + (v.pageY - g.pageY) * (v.pageY - g.pageY));
//                                 o || (o = w / s._currentZoom); var y = w / o; return L.call(s, y), void c(s.elements.zoomer)
//                             }
//                     h(d, m), f[i] = a.toString(), p(s.elements.preview, f), R.call(s), t = l, e = r
//                 }

//                 function f() { u(l = !1), window.removeEventListener("mousemove", m), window.removeEventListener("touchmove", m), window.removeEventListener("mouseup", f), window.removeEventListener("touchend", f), document.body.style[n] = "", B.call(s), Y.call(s), o = 0 }
//                 s.elements.overlay.addEventListener("mousedown", d), s.elements.viewport.addEventListener("keydown", function (e) {
//                     var t = 37,
//                         l = 38,
//                         u = 39,
//                         c = 40; if (!e.shiftKey || e.keyCode !== l && e.keyCode !== c) {
//                             if (s.options.enableKeyMovement && e.keyCode >= 37 && e.keyCode <= 40) {
//                                 e.preventDefault(); var d = function (e) {
//                                     switch (e) {
//                                         case t:
//                                             return [1, 0];
//                                         case l:
//                                             return [0, 1];
//                                         case u:
//                                             return [-1, 0];
//                                         case c:
//                                             return [0, -1]
//                                     }
//                                 }(e.keyCode);
//                                 a = w.parse(s.elements.preview), document.body.style[n] = "none", r = s.elements.viewport.getBoundingClientRect(),
//                                     function (e) {
//                                         var t = e[0],
//                                             r = e[1],
//                                             l = {};
//                                         h(t, r), l[i] = a.toString(), p(s.elements.preview, l), R.call(s), document.body.style[n] = "", B.call(s), Y.call(s), o = 0
//                                     }(d)
//                             }
//                         } else {
//                         var m = 0;
//                         m = e.keyCode === l ? parseFloat(s.elements.zoomer.value, 10) + parseFloat(s.elements.zoomer.step, 10) : parseFloat(s.elements.zoomer.value, 10) - parseFloat(s.elements.zoomer.step, 10), s.setZoom(m)
//                     }
//                 }), s.elements.overlay.addEventListener("touchstart", d)
//             }.call(this), this.options.enableZoom && function () {
//                 var e = this,
//                     t = e.elements.zoomerWrap = document.createElement("div"),
//                     i = e.elements.zoomer = document.createElement("input");

//                 function n() { _.call(e, { value: parseFloat(i.value), origin: new y(e.elements.preview), viewportRect: e.elements.viewport.getBoundingClientRect(), transform: w.parse(e.elements.preview) }) }

//                 function o(t) {
//                     var i, o; if ("ctrl" === e.options.mouseWheelZoom && !0 !== t.ctrlKey) return 0;
//                     i = t.wheelDelta ? t.wheelDelta / 1200 : t.deltaY ? t.deltaY / 1060 : t.detail ? t.detail / -60 : 0, o = e._currentZoom + i * e._currentZoom, t.preventDefault(), L.call(e, o), n.call(e)
//                 }
//                 d(t, ".-wrap"), d(i, "."), i.type = "range", i.step = "0.0001", i.value = 1, i.style.display = e.options.showZoomer ? "" : "none", i.setAttribute("aria-label", "zoom"), e.element.appendChild(t), t.appendChild(i), e._currentZoom = 1, e.elements.zoomer.addEventListener("input", n), e.elements.zoomer.addEventListener("change", n), e.options.mouseWheelZoom && (e.elements.boundary.addEventListener("mousewheel", o), e.elements.boundary.addEventListener("DOMMouseScroll", o))
//             }.call(this), this.options.enableResize && function () {
//                 var e, t, i, o, r, a, s, l = this,
//                     h = document.createElement("div"),
//                     u = !1,
//                     c = 50;
//                 d(h, "cr-resizer"), p(h, { width: this.options.viewport.width + "px", height: this.options.viewport.height + "px" }), this.options.resizeControls.height && (d(a = document.createElement("div"), "cr-resizer-vertical"), h.appendChild(a));
//                 this.options.resizeControls.width && (d(s = document.createElement("div"), "cr-resizer-horisontal"), h.appendChild(s));

//                 function m(a) {
//                     if ((void 0 === a.button || 0 === a.button) && (a.preventDefault(), !u)) {
//                         var s = l.elements.overlay.getBoundingClientRect(); if (u = !0, t = a.pageX, i = a.pageY, e = -1 !== a.currentTarget.className.indexOf("vertical") ? "v" : "h", o = s.width, r = s.height, a.touches) {
//                             var h = a.touches[0];
//                             t = h.pageX, i = h.pageY
//                         }
//                         window.addEventListener("mousemove", f), window.addEventListener("touchmove", f), window.addEventListener("mouseup", v), window.addEventListener("touchend", v), document.body.style[n] = "none"
//                     }
//                 }

//                 function f(n) {
//                     var a = n.pageX,
//                         s = n.pageY; if (n.preventDefault(), n.touches) {
//                             var u = n.touches[0];
//                             a = u.pageX, s = u.pageY
//                         } var d = a - t,
//                             m = s - i,
//                             f = l.options.viewport.height + m,
//                             v = l.options.viewport.width + d; "v" === e && f >= c && f <= r ? (p(h, { height: f + "px" }), l.options.boundary.height += m, p(l.elements.boundary, { height: l.options.boundary.height + "px" }), l.options.viewport.height += m, p(l.elements.viewport, { height: l.options.viewport.height + "px" })) : "h" === e && v >= c && v <= o && (p(h, { width: v + "px" }), l.options.boundary.width += d, p(l.elements.boundary, { width: l.options.boundary.width + "px" }), l.options.viewport.width += d, p(l.elements.viewport, { width: l.options.viewport.width + "px" })), R.call(l), k.call(l), B.call(l), Y.call(l), i = s, t = a
//                 }

//                 function v() { u = !1, window.removeEventListener("mousemove", f), window.removeEventListener("touchmove", f), window.removeEventListener("mouseup", v), window.removeEventListener("touchend", v), document.body.style[n] = "" }
//                 a && (a.addEventListener("mousedown", m), a.addEventListener("touchstart", m));
//                 s && (s.addEventListener("mousedown", m), s.addEventListener("touchstart", m));
//                 this.elements.boundary.appendChild(h)
//             }.call(this)
//     }

//     function E() { return this.options.enableExif && window.EXIF }

//     function L(e) {
//         if (this.options.enableZoom) {
//             var t = this.elements.zoomer,
//                 i = j(e, 4);
//             t.value = Math.max(t.min, Math.min(t.max, i))
//         }
//     }

//     function _(e) {
//         var n = this,
//             o = e ? e.transform : w.parse(n.elements.preview),
//             r = e ? e.viewportRect : n.elements.viewport.getBoundingClientRect(),
//             a = e ? e.origin : new y(n.elements.preview);

//         function s() {
//             var e = {};
//             e[i] = o.toString(), e[t] = a.toString(), p(n.elements.preview, e)
//         } if (n._currentZoom = e ? e.value : n._currentZoom, o.scale = n._currentZoom, n.elements.zoomer.setAttribute("aria-valuenow", n._currentZoom), s(), n.options.enforceBoundary) {
//             var l = function (e) {
//                 var t = this._currentZoom,
//                     i = e.width,
//                     n = e.height,
//                     o = this.elements.boundary.clientWidth / 2,
//                     r = this.elements.boundary.clientHeight / 2,
//                     a = this.elements.preview.getBoundingClientRect(),
//                     s = a.width,
//                     l = a.height,
//                     h = i / 2,
//                     u = n / 2,
//                     c = -1 * (h / t - o),
//                     p = -1 * (u / t - r),
//                     d = 1 / t * h,
//                     m = 1 / t * u; return { translate: { maxX: c, minX: c - (s * (1 / t) - i * (1 / t)), maxY: p, minY: p - (l * (1 / t) - n * (1 / t)) }, origin: { maxX: s * (1 / t) - d, minX: d, maxY: l * (1 / t) - m, minY: m } }
//             }.call(n, r),
//                 h = l.translate,
//                 u = l.origin;
//             o.x >= h.maxX && (a.x = u.minX, o.x = h.maxX), o.x <= h.minX && (a.x = u.maxX, o.x = h.minX), o.y >= h.maxY && (a.y = u.minY, o.y = h.maxY), o.y <= h.minY && (a.y = u.maxY, o.y = h.minY)
//         }
//         s(), X.call(n), Y.call(n)
//     }

//     function B() {
//         var e = this._currentZoom,
//             n = this.elements.preview.getBoundingClientRect(),
//             o = this.elements.viewport.getBoundingClientRect(),
//             r = w.parse(this.elements.preview.style[i]),
//             a = new y(this.elements.preview),
//             s = o.top - n.top + o.height / 2,
//             l = o.left - n.left + o.width / 2,
//             h = {},
//             u = {};
//         h.y = s / e, h.x = l / e, u.y = (h.y - a.y) * (1 - e), u.x = (h.x - a.x) * (1 - e), r.x -= u.x, r.y -= u.y; var c = {};
//         c[t] = h.x + "px " + h.y + "px", c[i] = r.toString(), p(this.elements.preview, c)
//     }

//     function R() {
//         if (this.elements) {
//             var e = this.elements.boundary.getBoundingClientRect(),
//                 t = this.elements.preview.getBoundingClientRect();
//             p(this.elements.overlay, { width: t.width + "px", height: t.height + "px", top: t.top - e.top + "px", left: t.left - e.left + "px" })
//         }
//     }
//     y.prototype.toString = function () { return this.x + "px " + this.y + "px" }; var Z, z, M, I, X = (Z = R, z = 500, function () {
//         var e = this,
//             t = arguments,
//             i = M && !I;
//         clearTimeout(I), I = setTimeout(function () { I = null, M || Z.apply(e, t) }, z), i && Z.apply(e, t)
//     });

//     function Y() {
//         var e, t = this.get();
//         F.call(this) && (this.options.update.call(this, t), this.$ && "undefined" == typeof Prototype ? this.$(this.element).trigger("update.croppie", t) : (window.CustomEvent ? e = new CustomEvent("update", { detail: t }) : (e = document.createEvent("CustomEvent")).initCustomEvent("update", !0, !0, t), this.element.dispatchEvent(e)))
//     }

//     function F() { return this.elements.preview.offsetHeight > 0 && this.elements.preview.offsetWidth > 0 }

//     function W() {
//         var e, n = {},
//             o = this.elements.preview,
//             r = new w(0, 0, 1),
//             a = new y;
//         F.call(this) && !this.data.bound && (this.data.bound = !0, n[i] = r.toString(), n[t] = a.toString(), n.opacity = 1, p(o, n), e = this.elements.preview.getBoundingClientRect(), this._originalImageWidth = e.width, this._originalImageHeight = e.height, this.data.orientation = b(this.elements.img), this.options.enableZoom ? k.call(this, !0) : this._currentZoom = 1, r.scale = this._currentZoom, n[i] = r.toString(), p(o, n), this.data.points.length ? function (e) {
//             if (4 !== e.length) throw "Croppie - Invalid number of points supplied: " + e; var n = e[2] - e[0],
//                 o = this.elements.viewport.getBoundingClientRect(),
//                 r = this.elements.boundary.getBoundingClientRect(),
//                 a = { left: o.left - r.left, top: o.top - r.top },
//                 s = o.width / n,
//                 l = e[1],
//                 h = e[0],
//                 u = -1 * e[1] + a.top,
//                 c = -1 * e[0] + a.left,
//                 d = {};
//             d[t] = h + "px " + l + "px", d[i] = new w(c, u, s).toString(), p(this.elements.preview, d), L.call(this, s), this._currentZoom = s
//         }.call(this, this.data.points) : function () {
//             var e = this.elements.preview.getBoundingClientRect(),
//                 t = this.elements.viewport.getBoundingClientRect(),
//                 n = this.elements.boundary.getBoundingClientRect(),
//                 o = t.left - n.left,
//                 r = t.top - n.top,
//                 a = o - (e.width - t.width) / 2,
//                 s = r - (e.height - t.height) / 2,
//                 l = new w(a, s, this._currentZoom);
//             p(this.elements.preview, i, l.toString())
//         }.call(this), B.call(this), R.call(this))
//     }

//     function k(e) {
//         var t, i, n, o, r = 0,
//             a = this.options.maxZoom || 1.5,
//             s = this.elements.zoomer,
//             l = parseFloat(s.value),
//             h = this.elements.boundary.getBoundingClientRect(),
//             u = v(this.elements.img, this.data.orientation),
//             p = this.elements.viewport.getBoundingClientRect();
//         this.options.enforceBoundary && (n = p.width / u.width, o = p.height / u.height, r = Math.max(n, o)), r >= a && (a = r + 1), s.min = j(r, 4), s.max = j(a, 4), !e && (l < s.min || l > s.max) ? L.call(this, l < s.min ? s.min : s.max) : e && (i = Math.max(h.width / u.width, h.height / u.height), t = null !== this.data.boundZoom ? this.data.boundZoom : i, L.call(this, t)), c(s)
//     }

//     function A(e) {
//         var t = e.points,
//             i = f(t[0]),
//             n = f(t[1]),
//             o = f(t[2]) - i,
//             r = f(t[3]) - n,
//             a = e.circle,
//             s = document.createElement("canvas"),
//             l = s.getContext("2d"),
//             h = e.outputWidth || o,
//             u = e.outputHeight || r;
//         e.outputWidth && e.outputHeight; return s.width = h, s.height = u, e.backgroundColor && (l.fillStyle = e.backgroundColor, l.fillRect(0, 0, h, u)), !1 !== this.options.enforceBoundary && (o = Math.min(o, this._originalImageWidth), r = Math.min(r, this._originalImageHeight)), l.drawImage(this.elements.preview, i, n, o, r, 0, 0, h, u), a && (l.fillStyle = "#fff", l.globalCompositeOperation = "destination-in", l.beginPath(), l.arc(s.width / 2, s.height / 2, s.width / 2, 0, 2 * Math.PI, !0), l.closePath(), l.fill()), s
//     }

//     function O(e, t) {
//         var i, n, o, r, a = this,
//             s = [],
//             l = null,
//             h = E.call(a); if ("string" == typeof e) i = e, e = {};
//         else if (Array.isArray(e)) s = e.slice();
//         else {
//             if (void 0 === e && a.data.url) return W.call(a), Y.call(a), null;
//             i = e.url, s = e.points || [], l = void 0 === e.zoom ? null : e.zoom
//         } return a.data.bound = !1, a.data.url = i || a.data.url, a.data.boundZoom = l, (n = i, o = h, r = new Image, r.style.opacity = 0, new Promise(function (e) {
//             function t() { r.style.opacity = 1, setTimeout(function () { e(r) }, 1) }
//             r.removeAttribute("crossOrigin"), n.match(/^https?:\/\/|^\/\//) && r.setAttribute("crossOrigin", "anonymous"), r.onload = function () { o ? EXIF.getData(r, function () { t() }) : t() }, r.src = n
//         })).then(function (i) {
//             if (function (e) { this.elements.img.parentNode && (Array.prototype.forEach.call(this.elements.img.classList, function (t) { e.classList.add(t) }), this.elements.img.parentNode.replaceChild(e, this.elements.img), this.elements.preview = e), this.elements.img = e }.call(a, i), s.length) a.options.relative && (s = [s[0] * i.naturalWidth / 100, s[1] * i.naturalHeight / 100, s[2] * i.naturalWidth / 100, s[3] * i.naturalHeight / 100]);
//             else {
//                 var n, o, r = v(i),
//                     l = a.elements.viewport.getBoundingClientRect(),
//                     h = l.width / l.height;
//                 r.width / r.height > h ? n = (o = r.height) * h : (n = r.width, o = r.height / h); var u = (r.width - n) / 2,
//                     c = (r.height - o) / 2,
//                     p = u + n,
//                     d = c + o;
//                 a.data.points = [u, c, p, d]
//             }
//             a.data.points = s.map(function (e) { return parseFloat(e) }), a.options.useCanvas && function (e) {
//                 var t = this.elements.canvas,
//                     i = this.elements.img,
//                     n = t.getContext("2d"),
//                     o = E.call(this);
//                 e = this.options.enableOrientation && e, n.clearRect(0, 0, t.width, t.height), t.width = i.width, t.height = i.height, o && !e ? x(t, i, f(b(i) || 0)) : e && x(t, i, e)
//             }.call(a, e.orientation || 1), W.call(a), Y.call(a), t && t()
//         }).catch(function (e) { console.error("Croppie:" + e) })
//     }

//     function j(e, t) { return parseFloat(e).toFixed(t || 0) }

//     function H() {
//         var e = this.elements.preview.getBoundingClientRect(),
//             t = this.elements.viewport.getBoundingClientRect(),
//             i = t.left - e.left,
//             n = t.top - e.top,
//             o = (t.width - this.elements.viewport.offsetWidth) / 2,
//             r = (t.height - this.elements.viewport.offsetHeight) / 2,
//             a = i + this.elements.viewport.offsetWidth + o,
//             s = n + this.elements.viewport.offsetHeight + r,
//             l = this._currentZoom;
//         (l === 1 / 0 || isNaN(l)) && (l = 1); var h = this.options.enforceBoundary ? 0 : Number.NEGATIVE_INFINITY; return i = Math.max(h, i / l), n = Math.max(h, n / l), a = Math.max(h, a / l), s = Math.max(h, s / l), { points: [j(i), j(n), j(a), j(s)], zoom: l, orientation: this.data.orientation }
//     } var N = { type: "canvas", format: "png", quality: 1 },
//         S = ["jpeg", "webp", "png"];

//     function P(e) {
//         var t = this,
//             i = H.call(t),
//             n = h(u(N), u(e)),
//             o = "string" == typeof e ? e : n.type || "base64",
//             r = n.size || "viewport",
//             a = n.format,
//             s = n.quality,
//             l = n.backgroundColor,
//             c = "boolean" == typeof n.circle ? n.circle : "circle" === t.options.viewport.type,
//             m = t.elements.viewport.getBoundingClientRect(),
//             f = m.width / m.height; return "viewport" === r ? (i.outputWidth = m.width, i.outputHeight = m.height) : "object" == typeof r && (r.width && r.height ? (i.outputWidth = r.width, i.outputHeight = r.height) : r.width ? (i.outputWidth = r.width, i.outputHeight = r.width / f) : r.height && (i.outputWidth = r.height * f, i.outputHeight = r.height)), S.indexOf(a) > -1 && (i.format = "image/" + a, i.quality = s), i.circle = c, i.url = t.data.url, i.backgroundColor = l, new Promise(function (e, n) {
//                 switch (o.toLowerCase()) {
//                     case "rawcanvas":
//                         e(A.call(t, i)); break;
//                     case "canvas":
//                     case "base64":
//                         e(function (e) { return A.call(this, e).toDataURL(e.format, e.quality) }.call(t, i)); break;
//                     case "blob":
//                         (function (e) { var t = this; return new Promise(function (i, n) { A.call(t, e).toBlob(function (e) { i(e) }, e.format, e.quality) }) }).call(t, i).then(e); break;
//                     default:
//                         e(function (e) {
//                             var t = e.points,
//                                 i = document.createElement("div"),
//                                 n = document.createElement("img"),
//                                 o = t[2] - t[0],
//                                 r = t[3] - t[1]; return d(i, "croppie-result"), i.appendChild(n), p(n, { left: -1 * t[0] + "px", top: -1 * t[1] + "px" }), n.src = e.url, p(i, { width: o + "px", height: r + "px" }), i
//                         }.call(t, i))
//                 }
//             })
//     }

//     function D(e) {
//         if (!this.options.useCanvas || !this.options.enableOrientation) throw "Croppie: Cannot rotate without enableOrientation && EXIF.js included"; var t, i, n, o, r, l = this.elements.canvas;
//         this.data.orientation = (t = this.data.orientation, i = e, n = a.indexOf(t) > -1 ? a : s, o = n.indexOf(t), r = i / 90 % n.length, n[(n.length + o + r % n.length) % n.length]), x(l, this.elements.img, this.data.orientation), k.call(this), _.call(this), copy = null
//     } if (window.jQuery) {
//         var T = window.jQuery;
//         T.fn.croppie = function (e) {
//             if ("string" === typeof e) {
//                 var t = Array.prototype.slice.call(arguments, 1),
//                     i = T(this).data("croppie"); return "get" === e ? i.get() : "result" === e ? i.result.apply(i, t) : "bind" === e ? i.bind.apply(i, t) : this.each(function () {
//                         var i = T(this).data("croppie"); if (i) {
//                             var n = i[e]; if (!T.isFunction(n)) throw "Croppie " + e + " method not found";
//                             n.apply(i, t), "destroy" === e && T(this).removeData("croppie")
//                         }
//                     })
//             } return this.each(function () {
//                 var t = new q(this, e);
//                 t.$ = T, T(this).data("croppie", t)
//             })
//         }
//     }

//     function q(e, t) {
//         if (e.className.indexOf("croppie-container") > -1) throw new Error("Croppie: Can't initialize croppie more than once"); if (this.element = e, this.options = h(u(q.defaults), t), "img" === this.element.tagName.toLowerCase()) {
//             var i = this.element;
//             d(i, "cr-original-image"), m(i, { "aria-hidden": "true", alt: "" }); var n = document.createElement("div");
//             this.element.parentNode.appendChild(n), n.appendChild(i), this.element = n, this.options.url = this.options.url || i.src
//         } if (C.call(this), this.options.url) {
//             var o = { url: this.options.url, points: this.options.points };
//             delete this.options.url, delete this.options.points, O.call(this, o)
//         }
//     }
//     q.defaults = { viewport: { width: 100, height: 100, type: "square" }, boundary: {}, orientationControls: { enabled: !0, leftClass: "", rightClass: "" }, resizeControls: { width: !0, height: !0 }, customClass: "", showZoomer: !0, enableZoom: !0, enableResize: !1, mouseWheelZoom: !0, enableExif: !1, enforceBoundary: !0, enableOrientation: !1, enableKeyMovement: !0, update: function () { } }, q.globals = { translate: "translate3d" }, h(q.prototype, {
//         bind: function (e, t) { return O.call(this, e, t) }, get: function () {
//             var e = H.call(this),
//                 t = e.points; return this.options.relative && (t[0] /= this.elements.img.naturalWidth / 100, t[1] /= this.elements.img.naturalHeight / 100, t[2] /= this.elements.img.naturalWidth / 100, t[3] /= this.elements.img.naturalHeight / 100), e
//         }, result: function (e) { return P.call(this, e) }, refresh: function () { return function () { W.call(this) }.call(this) }, setZoom: function (e) { L.call(this, e), c(this.elements.zoomer) }, rotate: function (e) { D.call(this, e) }, destroy: function () {
//             return function () {
//                 var e, t;
//                 this.element.removeChild(this.elements.boundary), e = this.element, t = "croppie-container", e.classList ? e.classList.remove(t) : e.className = e.className.replace(t, ""), this.options.enableZoom && this.element.removeChild(this.elements.zoomerWrap), delete this.elements
//             }.call(this)
//         }
//     }), e.Croppie = window.Croppie = q
// });

// jQuery(document).ready(function ($) {
//     $(window).load(function () {
//         // Animate loader off screen
//         $(".loader").hide();
//     });


//     /* ------------- fidback ----------------- */
//     document.addEventListener('DOMContentLoaded', () => {
//         function sendMessages(input1, input2) {
//             jQuery(".button-fidback").prop("disabled", true);
//             jQuery('.loader-request').css('display', 'block');
//             var part1 = jQuery('#' + input1).val();
//             var part2 = jQuery('#' + input2).val();

//             if ((part1.length > 0) && (part2.length > 0)) {
//                 jQuery.ajax({
//                     url: '',
//                     method: 'POST',
//                     data: { title_support: part1, content_support: part2 },
//                     success: function () {
//                         var elements = jQuery('.support-overlay, .support');
//                         jQuery(".button-fidback").prop("disabled", false);
//                         elements.removeClass('actives');
//                         jQuery('#' + input1).val('');
//                         jQuery('#' + input2).val('');
//                         //  jQuery( ".input-send" ).prop( "disabled", true );
//                         jQuery('.loader-request').css('display', 'none');
//                         var x = document.getElementById('toast1');
//                         x.className = "show";
//                         setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
//                         setTimeout(function () { location.reload(); }, 4000);
//                     }
//                 }).error(function () {
//                     //   jQuery( ".input-send" ).prop( "disabled", true );
//                     jQuery(".button-fidback").prop("disabled", false);
//                     jQuery('.loader-request').css('display', 'none');
//                     var x = document.getElementById("toast-err1");
//                     x.className = "show";
//                     setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
//                     setTimeout(function () { location.reload(); }, 4000);
//                 })
//             } else {
//                 jQuery(".button-fidback").prop("disabled", false);
//                 var x = document.getElementById("toast-not1");
//                 jQuery('.loader-request').css('display', 'none');
//                 x.className = "show";
//                 setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
//             }
//         };

//     })
//     /* ------------- Crop Images ----------------- */
//     jQuery(document).ready(function ($) {
//         var uploadCrop;
//         $("#avatarbox").click(function () {
//             $("#avatar").click();
//         })
//         uploadCrop = $('#imgs').croppie({
//             viewport: {
//                 width: 200,
//                 height: 200,
//             },
//         });

//         function readFileAvatar(input) {
//             if (input.files && input.files[0]) {
//                 var reader = new FileReader();
//                 reader.onload = function (e) {
//                     uploadCrop.croppie('bind', {
//                         url: e.target.result
//                     });
//                 }
//                 reader.readAsDataURL(input.files[0]);
//             } else {
//                 swal("Sorry - you're browser doesn't support the FileReader API");
//             }
//         }
//         $('#avatar').on('change', function () {
//             readFileAvatar(this);
//             $('.popup-frame').fadeIn();
//         });

//         $('#crop').on('click', function (ev) {
//             uploadCrop.croppie('result', {
//                 type: 'base64',
//                 format: 'jpeg',
//                 size: {
//                     width: 600,
//                     height: 600
//                 }
//             }).then(function (resp) {
//                 $('.img-avatar').attr('src', resp);
//                 $(".avatar-base64").val(resp);
//                 $("#avatar").prop('required', false).val("");
//                 $('.popup-frame').fadeOut();
//             });
//         });
//         $('.msg-text img,.closeicon').click(function () {
//             $(this).parent().parent().fadeOut();
//         });
//     });

//     /*------------- startup --------------- */

//     $(".cat-shetab:checked").each(function () {
//         $(".hiderahbar").toggle();
//     })
//     if ($(".cat-shetab:checked")) {

//     } else {

//     }
//     $(".cat-shetab").change(function () {
//         if ($(".cat-shetab:checked")) {
//             $(".hiderahbar").toggle();
//             $(".val").val("");
//         }
//         if (!$(".cat-shetab").is(':checked')) {

//             $(".val-shetab").val("");
//         }

//     });



//     $(".add-team").on("click", function () {
//         if ($('.group').length < 10) {
//             $('.clone').clone().addClass('group').removeClass('clone hide').insertBefore('.clone');
//         }
//     })

//     var uri = window.location.toString();
//     if (uri.indexOf("?") > 0) {
//         var clean_uri = uri.substring(0, uri.indexOf("?"));
//         window.history.replaceState({}, document.title, clean_uri);
//     }
//     $('.check-error').blur(function () {
//         var thisInput = $(this);
//         var dataValue = thisInput.val();
//         var dataType = thisInput.data('type');
//         $.ajax({
//             url: '',
//             method: 'POST',
//             data: {
//                 type: dataType,
//                 value: dataValue
//             },
//             success: function (response) {
//                 var error = $(response).filter('.notify').text();
//                 var errorArr = ['error_email'];
//                 if ($.inArray(error, errorArr) !== -1) {
//                     $('#' + error).show();
//                     thisInput.val('');
//                 } else $('.error-hide').hide();

//             }
//         })
//     });


//     Dropzone.prototype.defaultOptions.dictFallbackMessage = "مرورگر شما آپلود فایل drag'n'drop را پشتیبانی نمی کند.";
//     Dropzone.prototype.defaultOptions.dictFallbackText = "Please use the fallback form below to upload your files like in the olden days.";
//     Dropzone.prototype.defaultOptions.dictFileTooBig = "فایل خیلی بزرگ است ({{filesize}}MB)  حداکثر اندازه فایل: {{maxFilesize}}MB";
//     Dropzone.prototype.defaultOptions.dictInvalidFileType = "شما مجاز به بارگذاری این نوع فایل نیستید";
//     Dropzone.prototype.defaultOptions.dictResponseError = "Server responded with {{statusCode}} code.";
//     Dropzone.prototype.defaultOptions.dictCancelUpload = "انصراف از بارگذاری";
//     Dropzone.prototype.defaultOptions.dictCancelUploadConfirmation = "آیا مطمئن هستید که میخواهید این بارگذاری را لغو کنید؟";
//     Dropzone.prototype.defaultOptions.dictRemoveFile = "حذف فایل";
//     Dropzone.prototype.defaultOptions.dictRemoveFileConfirmation = null;
//     Dropzone.prototype.defaultOptions.dictMaxFilesExceeded = "شما فقط می توانید {{maxFiles}} فایل بارگذاری کنید  .";
//     Dropzone.prototype.defaultOptions.dictDefaultMessage = "برای بارگذاری فایل کلیک کنید";
//     Dropzone.options.uploadVideo = {
//         autoProcessQueue: true,
//         timeout: 1800000,
//         maxFiles: 1,
//         maxFilesize: 40, // MB
//         paramName: "video",
//         addRemoveLinks: true,
//         acceptedFiles: '.mp4,.mkv,.avi,.mov,.wmv',
//         init: function () {
//             var self = this;
//             this.on("success", function (file, responseText) {
//                 console.log(responseText);
//             });
//             this.on('error', function (file, response) {
//                 $('.text-error').text(response);
//                 $('.message-alert').fadeIn();
//                 $('.message-alert').delay(4000).fadeOut();
//             });
//             self.on("maxfilesexceeded", function (file) {
//                 self.removeAllFiles();
//                 self.addFile(file);
//             });
//             $("#send-video").click(function (e) {
//                 e.preventDefault();
//                 self.processQueue();
//             });
//             self.options.dictRemoveFile = "حذف";
//             self.on("addedfile", function (file) {

//             });
//             self.on("removedfile", function (file) {

//             });
//         }
//     }
//     document.querySelectorAll('.toggle-element').forEach(element => {
//         element.addEventListener('DOMSubtreeModified', () => {
//             const toggle1 = element.querySelector('[data-type="toggle-1"]');
//             if (toggle1) {
//                 const toggleButton = toggle1.querySelector('[data-type="toggle-btn"]');
//                 toggleButton.addEventListener('click', function () {
//                     toggle1.classList.add('hide');
//                     toggle2.classList.remove('hide');
//                 });
//             }
//             const toggle2 = element.querySelector('[data-type="toggle-2"]');


//         });
//     });
//     /*------------- LightBox --------------- */


//     $(".sg-tab").click(function () {
//         $tab_num = $(this).data("id");
//         if ($(this).hasClass("activee")) { } else {
//             $(".sg-tab").removeClass("activee");
//             $(this).addClass("activee");
//             $(".sg-content").hide();
//             $(".cnt" + $tab_num).fadeIn();
//         }
//     });


//     $('.province').each(function () {
//         var $province = $(this).data('value');
//         var $city = $('.city').data('value');
//         if ($province) {
//             $('.province option[value=' + $province + ']').attr('selected', 'selected');
//             $('.city').addClass("tempclass");
//             loadCity($province);
//             $('.city option[value=' + $city + ']').attr('selected', 'selected');
//         }
//     });






//     jQuery(document).ready(function ($) {
//         var elements = $('.support-overlay, .support');

//         $('.btn-support').click(function () {
//             elements.addClass('actives');
//         });

//         $('.close-support').click(function () {
//             elements.removeClass('actives');
//         });


//     });


//     /*---------- textarea characters ---------- */
//     function setCharCountListener() {
//         document.querySelectorAll(".char-count").forEach(element => {
//             const textArea = element.querySelector("textarea");
//             const holder = element.querySelector("p");
//             const maxlength = textArea.getAttribute("maxlength");

//             textArea.addEventListener("input", event => {
//                 holder.innerText = `${event.target.value.length}/${maxlength}`;
//             });
//             holder.innerText = `0/${maxlength}`;
//         });
//     }
//     setCharCountListener();
//     /*------------- ScrollToTop --------------- */
//     $(window).scroll(function () {
//         if ($(this).scrollTop() > 200) {
//             $(".scrollToTop").fadeIn();
//         } else {
//             $(".scrollToTop").fadeOut();
//         }
//     });
//     $(window).scroll(function () {
//         if ($(this).scrollTop() > 125) {
//             $(".susu").addClass("fixed");
//             $(".susu").addClass("fixed-sidebar-left");
//         } else {
//             $(".susu").removeClass("fixed");
//             $(".susu").removeClass("fixed-sidebar-left");
//         }
//     });
//     $(".scrollToTop").click(function () {
//         $("html, body").animate({
//             scrollTop: 0
//         },
//             800
//         );
//         return false;
//     });
//     $("#cssmenu li.active")
//         .addClass("open")
//         .children("ul")
//         .show();
//     $("#cssmenu li.has-sub>a").on("click", function () {
//         $(this).removeAttr("href");
//         var element = $(this).parent("li");
//         if (element.hasClass("open")) {
//             element.removeClass("open");
//             element.find("li").removeClass("open");
//             element.find("ul").slideUp(200);
//         } else {
//             element.addClass("open");
//             element.children("ul").slideDown(200);
//             element
//                 .siblings("li")
//                 .children("ul")
//                 .slideUp(200);
//             element.siblings("li").removeClass("open");
//             element
//                 .siblings("li")
//                 .find("li")
//                 .removeClass("open");
//             element
//                 .siblings("li")
//                 .find("ul")
//                 .slideUp(200);
//         }
//     });

//     $(".close-toggle").click(function () {
//         $(".menu-admin").css("width", "0px");
//         $(".box-admin").css("padding-right", "10px");
//         $(".close-toggle").addClass("open-toggle");
//         $(".close-toggle").removeClass();
//         $(".menu-admin").fadeOut(250);
//     });

//     $(".avatar-user").click(function () {
//         $(".dropd").fadeToggle(500);
//         $(".dropdlang").fadeToggle(500);
//     });
//     /*------------- MobileMenu --------------- */
//     $(".header-right-mob").click(function () {
//         $(".mob-swipe-bg").show();
//         value1 = $(".mobile-menu-right").css("right") === "-260px" ? 0 : "-260px";
//         $(".mobile-menu-right")
//             .stop()
//             .css({
//                 right: value1
//             });
//     });
//     $(".mob-swipe-bg").click(function () {
//         $(".mob-swipe-bg").hide();
//         $(".mobile-menu-right").css("right", "-260px");
//     });
//     $(".header-search-mob").click(function () {
//         $(".mobile-search").show("slow");
//         $(".mobile-search-input").focus();
//     });
//     $(".search-close").click(function () {
//         $(".mobile-search").hide("slow");
//     });

//     var maxLength = 280;
//     $("#team-excerpt").keyup(function () {
//         var length = $(this).val().length;
//         var length = maxLength - length;
//         $(".text-counter").text(length);
//     });
//     $("#team-excerpt1").keyup(function () {
//         var length = $(this).val().length;
//         var length = maxLength - length;
//         $(".text-counter1").text(length);
//     });
//     $("#team-excerpt2").keyup(function () {
//         var length = $(this).val().length;
//         var length = maxLength - length;
//         $(".text-counter2").text(length);
//     });


//     $("form").submit(function () {
//         $form = $("form");
//         if ($(".smart-validate").valid()) {
//             $(".loader").fadeIn();
//         }
//     });

//     /* ---------Ajax ------------*/

//     /* ---------- aleart  -----------*/
//     var fademessage = $(".message-producer")
//         .delay(3500)
//         .fadeOut();

//     /* ---------- step  -----------*/
//     $(".step").each(function (index, el) {
//         $(el)
//             .not(".active")
//             .addClass("done");
//         $(".done").html('<i class="icon-valid"></i>');
//         if ($(this).is(".active")) {
//             $(this)
//                 .parent()
//                 .addClass("pulse");
//             return false;
//         }
//     });


//     $(document).on("focus", ".datepicker", function () {
//         $(".datepicker").persianDatepicker({
//             format: "YYYY/MM/DD",
//             initialValue: false,
//             altField: ".datepicker-alt",
//         });

//     });
//     $(".datepicker-gregorian").persianDatepicker({
//         viewMode: 'year',
//         initialValueType: 'gregorian',
//         format: "YYYY/MM/DD",
//         initialValueType: 'persian'
//     });
//     $(".log-date").persianDatepicker({
//         altField: '#observer',
//         altFormat: "X",
//         observer: true,
//         format: 'YYYY/MM/DD',
//         timePicker: {
//             enabled: true
//         },
//     });
//     $(".log-date1").persianDatepicker({
//         altField: '#observer1',
//         altFormat: "X",
//         observer: true,
//         format: 'YYYY/MM/DD',
//         timePicker: {
//             enabled: true
//         },
//     });
//     $("#start-date").persianDatepicker({
//         format: "YYYY/MM/DD",
//         initialValue: false,
//         maxDate: new persianDate()
//     });
//     var i;
//     for (i = 0; i < 8; i++) {
//         $(".start-date" + i).persianDatepicker({
//             format: "YYYY-MM-DD",
//             altField: '.observer-start-date-alt' + i
//         });
//         $('.timepicker-s' + i).persianDatepicker({
//             onlyTimePicker: true,
//             format: "H:m",
//             initialValue: true,
//             altField: '.observer-timepicker-s-alt' + i
//         });

//         $('.timepicker-e' + i).persianDatepicker({
//             onlyTimePicker: true,
//             format: "H:m",
//             initialValue: true,
//             altField: '.observer-timepicker-e-alt' + i
//         });
//     }


//     $(".showhide").change(function () {
//         $show_id = $(this).data("show-id");
//         $(".hidden").hide();
//         if ($(this).is(":checked")) {
//             $("#" + $show_id).show();
//         }
//     });
//     $(".showhide").each(function () {
//         $show_id = $(this).data("show-id");
//         if ($(this).is(":checked")) {
//             $("#" + $show_id).show();
//         }
//     });
// });


// /* ---------- messages  -----------*/


// /* ---------- search roles  -----------*/
// function searchApi(id, resultId, name, path = null, companion) {

//     var searchRequest = null;
//     var resultid = resultId;
//     var _resultid = "'" + resultId + "'";
//     var param = name;
//     var _id = '.' + id;
//     var minlength = 2;
//     var refereeAPI = "http://127.0.0.1:2222/api/?";
//     var res = document.getElementById(resultid);
//     styleResult = 'searchresult';
//     if (path == 'startup') styleResult = 'searchresult2';
//     if (name == 'investor') styleResult = 'searchresult3';

//     clearTimeout(this.delay);
//     this.delay = setTimeout(function () {
//         var field, that = this,
//             value = jQuery(_id).val();

//         if (value.length >= minlength) {
//             jQuery(".start-load").show();
//             console.log("test-12");
//             args = {
//                 type: param,
//                 fields: value,
//                 companion: companion
//             };
//             jQuery.getJSON(refereeAPI, args).done(function (data) {
//                 res.innerHTML = "";
//                 if (data.length) {
//                     jQuery(".start-load").hide();
//                     var output = '<ul class="' + styleResult + '">';
//                     jQuery.each(data, function (i, item) {
//                         output += '<li  data-id="' + item.id + '" data-name="' + item.name + '">';
//                         output += '<span>' + item.name + '</span>';
//                         output += '</li>';
//                         if (i === 8) {
//                             return false;
//                         }
//                     });
//                     output += '</ul>';
//                     res.style.display = "block";
//                     res.innerHTML = output;
//                     res.firstElementChild.style.display = "block";

//                     // jQuery(that).closest('.'+resultId).append(output);
//                 } else {
//                     // jQuery(that).closest('.'+resultId).append('<span class="font-s14">ŁŲ±ŲÆŪ ŲØŲ§ Ų§ŪŁ† Ł†Ų§Ł… Ł¾ŪŲÆŲ§ Ł†Ų´ŲÆ</span>');
//                     jQuery(".start-load").hide();
//                     var output = '<ul class="' + styleResult + '">';
//                     output += '<li>';
//                     output += '<span class="font-s14">فردی با این نام پیدا نشد</span>';
//                     output += '</li>';
//                     if (path == 'startup') {
//                         output += '<li>';
//                         output += '<span class="font-s14 create-leader btn-web align-center margin-auto spacer-r38"><i class="fa fa-plus-circle font-s10 pad-l10"></i>Ų§ŁŲ²ŁŲÆŁ† Ų±Ų§Ł‡ŲØŲ± Ų¬ŲÆŪŲÆ</span>';
//                         output += '</li>';
//                     }
//                     res.style.display = "block";
//                     res.innerHTML = output;
//                     res.firstElementChild.style.display = "block";
//                 }
//             }).fail(function () {
//                 console.log("error");
//             }).always(function () {

//             });
//         } else {
//             res.innerHTML = "";
//             // res.style.display = "none";
//             // jQuery(that).siblings('.'+resultid).html('').hide();
//         }
//     }.bind(this), 500);

//     jQuery(document).on('click', '#' + resultid + ' .' + styleResult + ' li', function ($) {
//         var id = jQuery(this).data("id");
//         var name = jQuery(this).data("name");
//         jQuery(this).parents().eq(2).find('.choosen-name').val(name);
//         jQuery(this).parents().eq(2).find('.choosen-id').val(id).trigger('change');
//         res.style.display = "none";
//     })
// }


! function (e, t) { "function" == typeof define && define.amd ? define(["exports"], t) : "object" == typeof exports && "string" != typeof exports.nodeName ? t(exports) : t(e.commonJsStrict = {}) }(this, function (e) {
    "function" != typeof Promise && function (e) {
        function t(e, t) { return function () { e.apply(t, arguments) } }

        function i(e) {
            if ("object" != typeof this) throw new TypeError("Promises must be constructed via new"); if ("function" != typeof e) throw new TypeError("not a function");
            this._state = null, this._value = null, this._deferreds = [], s(e, t(o, this), t(r, this))
        }

        function n(e) {
            var t = this; return null === this._state ? void this._deferreds.push(e) : void h(function () {
                var i = t._state ? e.onFulfilled : e.onRejected; if (null !== i) {
                    var n; try { n = i(t._value) } catch (t) { return void e.reject(t) }
                    e.resolve(n)
                } else (t._state ? e.resolve : e.reject)(t._value)
            })
        }

        function o(e) {
            try {
                if (e === this) throw new TypeError("A promise cannot be resolved with itself."); if (e && ("object" == typeof e || "function" == typeof e)) { var i = e.then; if ("function" == typeof i) return void s(t(i, e), t(o, this), t(r, this)) }
                this._state = !0, this._value = e, a.call(this)
            } catch (e) { r.call(this, e) }
        }

        function r(e) { this._state = !1, this._value = e, a.call(this) }

        function a() {
            for (var e = 0, t = this._deferreds.length; t > e; e++) n.call(this, this._deferreds[e]);
            this._deferreds = null
        }

        function s(e, t, i) {
            var n = !1; try { e(function (e) { n || (n = !0, t(e)) }, function (e) { n || (n = !0, i(e)) }) } catch (e) {
                if (n) return;
                n = !0, i(e)
            }
        } var l = setTimeout,
            h = "function" == typeof setImmediate && setImmediate || function (e) { l(e, 1) },
            u = Array.isArray || function (e) { return "[object Array]" === Object.prototype.toString.call(e) };
        i.prototype.catch = function (e) { return this.then(null, e) }, i.prototype.then = function (e, t) { var o = this; return new i(function (i, r) { n.call(o, new function (e, t, i, n) { this.onFulfilled = "function" == typeof e ? e : null, this.onRejected = "function" == typeof t ? t : null, this.resolve = i, this.reject = n }(e, t, i, r)) }) }, i.all = function () {
            var e = Array.prototype.slice.call(1 === arguments.length && u(arguments[0]) ? arguments[0] : arguments); return new i(function (t, i) {
                function n(r, a) {
                    try {
                        if (a && ("object" == typeof a || "function" == typeof a)) { var s = a.then; if ("function" == typeof s) return void s.call(a, function (e) { n(r, e) }, i) }
                        e[r] = a, 0 == --o && t(e)
                    } catch (e) { i(e) }
                } if (0 === e.length) return t([]); for (var o = e.length, r = 0; r < e.length; r++) n(r, e[r])
            })
        }, i.resolve = function (e) { return e && "object" == typeof e && e.constructor === i ? e : new i(function (t) { t(e) }) }, i.reject = function (e) { return new i(function (t, i) { i(e) }) }, i.race = function (e) { return new i(function (t, i) { for (var n = 0, o = e.length; o > n; n++) e[n].then(t, i) }) }, i._setImmediateFn = function (e) { h = e }, "undefined" != typeof module && module.exports ? module.exports = i : e.Promise || (e.Promise = i)
    }(this), "function" != typeof window.CustomEvent && function () {
        function e(e, t) { t = t || { bubbles: !1, cancelable: !1, detail: void 0 }; var i = document.createEvent("CustomEvent"); return i.initCustomEvent(e, t.bubbles, t.cancelable, t.detail), i }
        e.prototype = window.Event.prototype, window.CustomEvent = e
    }(), HTMLCanvasElement.prototype.toBlob || Object.defineProperty(HTMLCanvasElement.prototype, "toBlob", {
        value: function (e, t, i) {
            for (var n = atob(this.toDataURL(t, i).split(",")[1]), o = n.length, r = new Uint8Array(o), a = 0; a < o; a++) r[a] = n.charCodeAt(a);
            e(new Blob([r], { type: t || "image/png" }))
        }
    }); var t, i, n, o = ["Webkit", "Moz", "ms"],
        r = document.createElement("div").style,
        a = [1, 8, 3, 6],
        s = [2, 7, 4, 5];

    function l(e) {
        if (e in r) return e; for (var t = e[0].toUpperCase() + e.slice(1), i = o.length; i--;)
            if ((e = o[i] + t) in r) return e
    }

    function h(e, t) { e = e || {}; for (var i in t) t[i] && t[i].constructor && t[i].constructor === Object ? (e[i] = e[i] || {}, h(e[i], t[i])) : e[i] = t[i]; return e }

    function u(e) { return h({}, e) }

    function c(e) {
        if ("createEvent" in document) {
            var t = document.createEvent("HTMLEvents");
            t.initEvent("change", !1, !0), e.dispatchEvent(t)
        } else e.fireEvent("onchange")
    }

    function p(e, t, i) {
        if ("string" == typeof t) {
            var n = t;
            (t = {})[n] = i
        } for (var o in t) e.style[o] = t[o]
    }

    function d(e, t) { e.classList ? e.classList.add(t) : e.className += " " + t }

    function m(e, t) { for (var i in t) e.setAttribute(i, t[i]) }

    function f(e) { return parseInt(e, 10) }

    function v(e, t) {
        var i = e.naturalWidth,
            n = e.naturalHeight,
            o = t || b(e); if (o && o >= 5) {
                var r = i;
                i = n, n = r
            } return { width: i, height: n }
    }
    i = l("transform"), t = l("transformOrigin"), n = l("userSelect"); var g = { translate3d: { suffix: ", 0px" }, translate: { suffix: "" } },
        w = function (e, t, i) { this.x = parseFloat(e), this.y = parseFloat(t), this.scale = parseFloat(i) };
    w.parse = function (e) { return e.style ? w.parse(e.style[i]) : e.indexOf("matrix") > -1 || e.indexOf("none") > -1 ? w.fromMatrix(e) : w.fromString(e) }, w.fromMatrix = function (e) { var t = e.substring(7).split(","); return t.length && "none" !== e || (t = [1, 0, 0, 1, 0, 0]), new w(f(t[4]), f(t[5]), parseFloat(t[0])) }, w.fromString = function (e) {
        var t = e.split(") "),
            i = t[0].substring(q.globals.translate.length + 1).split(","),
            n = t.length > 1 ? t[1].substring(6) : 1,
            o = i.length > 1 ? i[0] : 0,
            r = i.length > 1 ? i[1] : 0; return new w(o, r, n)
    }, w.prototype.toString = function () { var e = g[q.globals.translate].suffix || ""; return q.globals.translate + "(" + this.x + "px, " + this.y + "px" + e + ") scale(" + this.scale + ")" }; var y = function (e) {
        if (!e || !e.style[t]) return this.x = 0, void (this.y = 0); var i = e.style[t].split(" ");
        this.x = parseFloat(i[0]), this.y = parseFloat(i[1])
    };

    function b(e) { return e.exifdata ? e.exifdata.Orientation : 1 }

    function x(e, t, i) {
        var n = t.width,
            o = t.height,
            r = e.getContext("2d"); switch (e.width = t.width, e.height = t.height, r.save(), i) {
                case 2:
                    r.translate(n, 0), r.scale(-1, 1); break;
                case 3:
                    r.translate(n, o), r.rotate(180 * Math.PI / 180); break;
                case 4:
                    r.translate(0, o), r.scale(1, -1); break;
                case 5:
                    e.width = o, e.height = n, r.rotate(90 * Math.PI / 180), r.scale(1, -1); break;
                case 6:
                    e.width = o, e.height = n, r.rotate(90 * Math.PI / 180), r.translate(0, -o); break;
                case 7:
                    e.width = o, e.height = n, r.rotate(-90 * Math.PI / 180), r.translate(-n, o), r.scale(1, -1); break;
                case 8:
                    e.width = o, e.height = n, r.translate(0, n), r.rotate(-90 * Math.PI / 180)
            }
        r.drawImage(t, 0, 0, n, o), r.restore()
    }

    function C() {
        var e, t, o, r, a, s = this.options.viewport.type ? "cr-vp-" + this.options.viewport.type : null;
        this.options.useCanvas = this.options.enableOrientation || E.call(this), this.data = {}, this.elements = {}, e = this.elements.boundary = document.createElement("div"), t = this.elements.viewport = document.createElement("div"), this.elements.img = document.createElement("img"), o = this.elements.overlay = document.createElement("div"), this.options.useCanvas ? (this.elements.canvas = document.createElement("canvas"), this.elements.preview = this.elements.canvas) : this.elements.preview = this.elements.img, d(e, "cr-boundary"), e.setAttribute("aria-dropeffect", "none"), r = this.options.boundary.width, a = this.options.boundary.height, p(e, { width: r + (isNaN(r) ? "" : "px"), height: a + (isNaN(a) ? "" : "px") }), d(t, "cr-viewport"), s && d(t, s), p(t, { width: this.options.viewport.width + "px", height: this.options.viewport.height + "px" }), t.setAttribute("tabindex", 0), d(this.elements.preview, "cr-image"), m(this.elements.preview, { alt: "preview", "aria-grabbed": "false" }), d(o, "cr-overlay"), this.element.appendChild(e), e.appendChild(this.elements.preview), e.appendChild(t), e.appendChild(o), d(this.element, "croppie-container"), this.options.customClass && d(this.element, this.options.customClass),
            function () {
                var e, t, o, r, a, s = this,
                    l = !1;

                function h(e, t) {
                    var i = s.elements.preview.getBoundingClientRect(),
                        n = a.y + t,
                        o = a.x + e;
                    s.options.enforceBoundary ? (r.top > i.top + t && r.bottom < i.bottom + t && (a.y = n), r.left > i.left + e && r.right < i.right + e && (a.x = o)) : (a.y = n, a.x = o)
                }

                function u(e) { s.elements.preview.setAttribute("aria-grabbed", e), s.elements.boundary.setAttribute("aria-dropeffect", e ? "move" : "none") }

                function d(i) {
                    if ((void 0 === i.button || 0 === i.button) && (i.preventDefault(), !l)) {
                        if (l = !0, e = i.pageX, t = i.pageY, i.touches) {
                            var o = i.touches[0];
                            e = o.pageX, t = o.pageY
                        }
                        u(l), a = w.parse(s.elements.preview), window.addEventListener("mousemove", m), window.addEventListener("touchmove", m), window.addEventListener("mouseup", f), window.addEventListener("touchend", f), document.body.style[n] = "none", r = s.elements.viewport.getBoundingClientRect()
                    }
                }

                function m(n) {
                    n.preventDefault(); var r = n.pageX,
                        l = n.pageY; if (n.touches) {
                            var u = n.touches[0];
                            r = u.pageX, l = u.pageY
                        } var d = r - e,
                            m = l - t,
                            f = {}; if ("touchmove" === n.type && n.touches.length > 1) {
                                var v = n.touches[0],
                                    g = n.touches[1],
                                    w = Math.sqrt((v.pageX - g.pageX) * (v.pageX - g.pageX) + (v.pageY - g.pageY) * (v.pageY - g.pageY));
                                o || (o = w / s._currentZoom); var y = w / o; return L.call(s, y), void c(s.elements.zoomer)
                            }
                    h(d, m), f[i] = a.toString(), p(s.elements.preview, f), R.call(s), t = l, e = r
                }

                function f() { u(l = !1), window.removeEventListener("mousemove", m), window.removeEventListener("touchmove", m), window.removeEventListener("mouseup", f), window.removeEventListener("touchend", f), document.body.style[n] = "", B.call(s), Y.call(s), o = 0 }
                s.elements.overlay.addEventListener("mousedown", d), s.elements.viewport.addEventListener("keydown", function (e) {
                    var t = 37,
                        l = 38,
                        u = 39,
                        c = 40; if (!e.shiftKey || e.keyCode !== l && e.keyCode !== c) {
                            if (s.options.enableKeyMovement && e.keyCode >= 37 && e.keyCode <= 40) {
                                e.preventDefault(); var d = function (e) {
                                    switch (e) {
                                        case t:
                                            return [1, 0];
                                        case l:
                                            return [0, 1];
                                        case u:
                                            return [-1, 0];
                                        case c:
                                            return [0, -1]
                                    }
                                }(e.keyCode);
                                a = w.parse(s.elements.preview), document.body.style[n] = "none", r = s.elements.viewport.getBoundingClientRect(),
                                    function (e) {
                                        var t = e[0],
                                            r = e[1],
                                            l = {};
                                        h(t, r), l[i] = a.toString(), p(s.elements.preview, l), R.call(s), document.body.style[n] = "", B.call(s), Y.call(s), o = 0
                                    }(d)
                            }
                        } else {
                        var m = 0;
                        m = e.keyCode === l ? parseFloat(s.elements.zoomer.value, 10) + parseFloat(s.elements.zoomer.step, 10) : parseFloat(s.elements.zoomer.value, 10) - parseFloat(s.elements.zoomer.step, 10), s.setZoom(m)
                    }
                }), s.elements.overlay.addEventListener("touchstart", d)
            }.call(this), this.options.enableZoom && function () {
                var e = this,
                    t = e.elements.zoomerWrap = document.createElement("div"),
                    i = e.elements.zoomer = document.createElement("input");

                function n() { _.call(e, { value: parseFloat(i.value), origin: new y(e.elements.preview), viewportRect: e.elements.viewport.getBoundingClientRect(), transform: w.parse(e.elements.preview) }) }

                function o(t) {
                    var i, o; if ("ctrl" === e.options.mouseWheelZoom && !0 !== t.ctrlKey) return 0;
                    i = t.wheelDelta ? t.wheelDelta / 1200 : t.deltaY ? t.deltaY / 1060 : t.detail ? t.detail / -60 : 0, o = e._currentZoom + i * e._currentZoom, t.preventDefault(), L.call(e, o), n.call(e)
                }
                d(t, ".-wrap"), d(i, "."), i.type = "range", i.step = "0.0001", i.value = 1, i.style.display = e.options.showZoomer ? "" : "none", i.setAttribute("aria-label", "zoom"), e.element.appendChild(t), t.appendChild(i), e._currentZoom = 1, e.elements.zoomer.addEventListener("input", n), e.elements.zoomer.addEventListener("change", n), e.options.mouseWheelZoom && (e.elements.boundary.addEventListener("mousewheel", o), e.elements.boundary.addEventListener("DOMMouseScroll", o))
            }.call(this), this.options.enableResize && function () {
                var e, t, i, o, r, a, s, l = this,
                    h = document.createElement("div"),
                    u = !1,
                    c = 50;
                d(h, "cr-resizer"), p(h, { width: this.options.viewport.width + "px", height: this.options.viewport.height + "px" }), this.options.resizeControls.height && (d(a = document.createElement("div"), "cr-resizer-vertical"), h.appendChild(a));
                this.options.resizeControls.width && (d(s = document.createElement("div"), "cr-resizer-horisontal"), h.appendChild(s));

                function m(a) {
                    if ((void 0 === a.button || 0 === a.button) && (a.preventDefault(), !u)) {
                        var s = l.elements.overlay.getBoundingClientRect(); if (u = !0, t = a.pageX, i = a.pageY, e = -1 !== a.currentTarget.className.indexOf("vertical") ? "v" : "h", o = s.width, r = s.height, a.touches) {
                            var h = a.touches[0];
                            t = h.pageX, i = h.pageY
                        }
                        window.addEventListener("mousemove", f), window.addEventListener("touchmove", f), window.addEventListener("mouseup", v), window.addEventListener("touchend", v), document.body.style[n] = "none"
                    }
                }

                function f(n) {
                    var a = n.pageX,
                        s = n.pageY; if (n.preventDefault(), n.touches) {
                            var u = n.touches[0];
                            a = u.pageX, s = u.pageY
                        } var d = a - t,
                            m = s - i,
                            f = l.options.viewport.height + m,
                            v = l.options.viewport.width + d; "v" === e && f >= c && f <= r ? (p(h, { height: f + "px" }), l.options.boundary.height += m, p(l.elements.boundary, { height: l.options.boundary.height + "px" }), l.options.viewport.height += m, p(l.elements.viewport, { height: l.options.viewport.height + "px" })) : "h" === e && v >= c && v <= o && (p(h, { width: v + "px" }), l.options.boundary.width += d, p(l.elements.boundary, { width: l.options.boundary.width + "px" }), l.options.viewport.width += d, p(l.elements.viewport, { width: l.options.viewport.width + "px" })), R.call(l), k.call(l), B.call(l), Y.call(l), i = s, t = a
                }

                function v() { u = !1, window.removeEventListener("mousemove", f), window.removeEventListener("touchmove", f), window.removeEventListener("mouseup", v), window.removeEventListener("touchend", v), document.body.style[n] = "" }
                a && (a.addEventListener("mousedown", m), a.addEventListener("touchstart", m));
                s && (s.addEventListener("mousedown", m), s.addEventListener("touchstart", m));
                this.elements.boundary.appendChild(h)
            }.call(this)
    }

    function E() { return this.options.enableExif && window.EXIF }

    function L(e) {
        if (this.options.enableZoom) {
            var t = this.elements.zoomer,
                i = j(e, 4);
            t.value = Math.max(t.min, Math.min(t.max, i))
        }
    }

    function _(e) {
        var n = this,
            o = e ? e.transform : w.parse(n.elements.preview),
            r = e ? e.viewportRect : n.elements.viewport.getBoundingClientRect(),
            a = e ? e.origin : new y(n.elements.preview);

        function s() {
            var e = {};
            e[i] = o.toString(), e[t] = a.toString(), p(n.elements.preview, e)
        } if (n._currentZoom = e ? e.value : n._currentZoom, o.scale = n._currentZoom, n.elements.zoomer.setAttribute("aria-valuenow", n._currentZoom), s(), n.options.enforceBoundary) {
            var l = function (e) {
                var t = this._currentZoom,
                    i = e.width,
                    n = e.height,
                    o = this.elements.boundary.clientWidth / 2,
                    r = this.elements.boundary.clientHeight / 2,
                    a = this.elements.preview.getBoundingClientRect(),
                    s = a.width,
                    l = a.height,
                    h = i / 2,
                    u = n / 2,
                    c = -1 * (h / t - o),
                    p = -1 * (u / t - r),
                    d = 1 / t * h,
                    m = 1 / t * u; return { translate: { maxX: c, minX: c - (s * (1 / t) - i * (1 / t)), maxY: p, minY: p - (l * (1 / t) - n * (1 / t)) }, origin: { maxX: s * (1 / t) - d, minX: d, maxY: l * (1 / t) - m, minY: m } }
            }.call(n, r),
                h = l.translate,
                u = l.origin;
            o.x >= h.maxX && (a.x = u.minX, o.x = h.maxX), o.x <= h.minX && (a.x = u.maxX, o.x = h.minX), o.y >= h.maxY && (a.y = u.minY, o.y = h.maxY), o.y <= h.minY && (a.y = u.maxY, o.y = h.minY)
        }
        s(), X.call(n), Y.call(n)
    }

    function B() {
        var e = this._currentZoom,
            n = this.elements.preview.getBoundingClientRect(),
            o = this.elements.viewport.getBoundingClientRect(),
            r = w.parse(this.elements.preview.style[i]),
            a = new y(this.elements.preview),
            s = o.top - n.top + o.height / 2,
            l = o.left - n.left + o.width / 2,
            h = {},
            u = {};
        h.y = s / e, h.x = l / e, u.y = (h.y - a.y) * (1 - e), u.x = (h.x - a.x) * (1 - e), r.x -= u.x, r.y -= u.y; var c = {};
        c[t] = h.x + "px " + h.y + "px", c[i] = r.toString(), p(this.elements.preview, c)
    }

    function R() {
        if (this.elements) {
            var e = this.elements.boundary.getBoundingClientRect(),
                t = this.elements.preview.getBoundingClientRect();
            p(this.elements.overlay, { width: t.width + "px", height: t.height + "px", top: t.top - e.top + "px", left: t.left - e.left + "px" })
        }
    }
    y.prototype.toString = function () { return this.x + "px " + this.y + "px" }; var Z, z, M, I, X = (Z = R, z = 500, function () {
        var e = this,
            t = arguments,
            i = M && !I;
        clearTimeout(I), I = setTimeout(function () { I = null, M || Z.apply(e, t) }, z), i && Z.apply(e, t)
    });

    function Y() {
        var e, t = this.get();
        F.call(this) && (this.options.update.call(this, t), this.$ && "undefined" == typeof Prototype ? this.$(this.element).trigger("update.croppie", t) : (window.CustomEvent ? e = new CustomEvent("update", { detail: t }) : (e = document.createEvent("CustomEvent")).initCustomEvent("update", !0, !0, t), this.element.dispatchEvent(e)))
    }

    function F() { return this.elements.preview.offsetHeight > 0 && this.elements.preview.offsetWidth > 0 }

    function W() {
        var e, n = {},
            o = this.elements.preview,
            r = new w(0, 0, 1),
            a = new y;
        F.call(this) && !this.data.bound && (this.data.bound = !0, n[i] = r.toString(), n[t] = a.toString(), n.opacity = 1, p(o, n), e = this.elements.preview.getBoundingClientRect(), this._originalImageWidth = e.width, this._originalImageHeight = e.height, this.data.orientation = b(this.elements.img), this.options.enableZoom ? k.call(this, !0) : this._currentZoom = 1, r.scale = this._currentZoom, n[i] = r.toString(), p(o, n), this.data.points.length ? function (e) {
            if (4 !== e.length) throw "Croppie - Invalid number of points supplied: " + e; var n = e[2] - e[0],
                o = this.elements.viewport.getBoundingClientRect(),
                r = this.elements.boundary.getBoundingClientRect(),
                a = { left: o.left - r.left, top: o.top - r.top },
                s = o.width / n,
                l = e[1],
                h = e[0],
                u = -1 * e[1] + a.top,
                c = -1 * e[0] + a.left,
                d = {};
            d[t] = h + "px " + l + "px", d[i] = new w(c, u, s).toString(), p(this.elements.preview, d), L.call(this, s), this._currentZoom = s
        }.call(this, this.data.points) : function () {
            var e = this.elements.preview.getBoundingClientRect(),
                t = this.elements.viewport.getBoundingClientRect(),
                n = this.elements.boundary.getBoundingClientRect(),
                o = t.left - n.left,
                r = t.top - n.top,
                a = o - (e.width - t.width) / 2,
                s = r - (e.height - t.height) / 2,
                l = new w(a, s, this._currentZoom);
            p(this.elements.preview, i, l.toString())
        }.call(this), B.call(this), R.call(this))
    }

    function k(e) {
        var t, i, n, o, r = 0,
            a = this.options.maxZoom || 1.5,
            s = this.elements.zoomer,
            l = parseFloat(s.value),
            h = this.elements.boundary.getBoundingClientRect(),
            u = v(this.elements.img, this.data.orientation),
            p = this.elements.viewport.getBoundingClientRect();
        this.options.enforceBoundary && (n = p.width / u.width, o = p.height / u.height, r = Math.max(n, o)), r >= a && (a = r + 1), s.min = j(r, 4), s.max = j(a, 4), !e && (l < s.min || l > s.max) ? L.call(this, l < s.min ? s.min : s.max) : e && (i = Math.max(h.width / u.width, h.height / u.height), t = null !== this.data.boundZoom ? this.data.boundZoom : i, L.call(this, t)), c(s)
    }

    function A(e) {
        var t = e.points,
            i = f(t[0]),
            n = f(t[1]),
            o = f(t[2]) - i,
            r = f(t[3]) - n,
            a = e.circle,
            s = document.createElement("canvas"),
            l = s.getContext("2d"),
            h = e.outputWidth || o,
            u = e.outputHeight || r;
        e.outputWidth && e.outputHeight; return s.width = h, s.height = u, e.backgroundColor && (l.fillStyle = e.backgroundColor, l.fillRect(0, 0, h, u)), !1 !== this.options.enforceBoundary && (o = Math.min(o, this._originalImageWidth), r = Math.min(r, this._originalImageHeight)), l.drawImage(this.elements.preview, i, n, o, r, 0, 0, h, u), a && (l.fillStyle = "#fff", l.globalCompositeOperation = "destination-in", l.beginPath(), l.arc(s.width / 2, s.height / 2, s.width / 2, 0, 2 * Math.PI, !0), l.closePath(), l.fill()), s
    }

    function O(e, t) {
        var i, n, o, r, a = this,
            s = [],
            l = null,
            h = E.call(a); if ("string" == typeof e) i = e, e = {};
        else if (Array.isArray(e)) s = e.slice();
        else {
            if (void 0 === e && a.data.url) return W.call(a), Y.call(a), null;
            i = e.url, s = e.points || [], l = void 0 === e.zoom ? null : e.zoom
        } return a.data.bound = !1, a.data.url = i || a.data.url, a.data.boundZoom = l, (n = i, o = h, r = new Image, r.style.opacity = 0, new Promise(function (e) {
            function t() { r.style.opacity = 1, setTimeout(function () { e(r) }, 1) }
            r.removeAttribute("crossOrigin"), n.match(/^https?:\/\/|^\/\//) && r.setAttribute("crossOrigin", "anonymous"), r.onload = function () { o ? EXIF.getData(r, function () { t() }) : t() }, r.src = n
        })).then(function (i) {
            if (function (e) { this.elements.img.parentNode && (Array.prototype.forEach.call(this.elements.img.classList, function (t) { e.classList.add(t) }), this.elements.img.parentNode.replaceChild(e, this.elements.img), this.elements.preview = e), this.elements.img = e }.call(a, i), s.length) a.options.relative && (s = [s[0] * i.naturalWidth / 100, s[1] * i.naturalHeight / 100, s[2] * i.naturalWidth / 100, s[3] * i.naturalHeight / 100]);
            else {
                var n, o, r = v(i),
                    l = a.elements.viewport.getBoundingClientRect(),
                    h = l.width / l.height;
                r.width / r.height > h ? n = (o = r.height) * h : (n = r.width, o = r.height / h); var u = (r.width - n) / 2,
                    c = (r.height - o) / 2,
                    p = u + n,
                    d = c + o;
                a.data.points = [u, c, p, d]
            }
            a.data.points = s.map(function (e) { return parseFloat(e) }), a.options.useCanvas && function (e) {
                var t = this.elements.canvas,
                    i = this.elements.img,
                    n = t.getContext("2d"),
                    o = E.call(this);
                e = this.options.enableOrientation && e, n.clearRect(0, 0, t.width, t.height), t.width = i.width, t.height = i.height, o && !e ? x(t, i, f(b(i) || 0)) : e && x(t, i, e)
            }.call(a, e.orientation || 1), W.call(a), Y.call(a), t && t()
        }).catch(function (e) { console.error("Croppie:" + e) })
    }

    function j(e, t) { return parseFloat(e).toFixed(t || 0) }

    function H() {
        var e = this.elements.preview.getBoundingClientRect(),
            t = this.elements.viewport.getBoundingClientRect(),
            i = t.left - e.left,
            n = t.top - e.top,
            o = (t.width - this.elements.viewport.offsetWidth) / 2,
            r = (t.height - this.elements.viewport.offsetHeight) / 2,
            a = i + this.elements.viewport.offsetWidth + o,
            s = n + this.elements.viewport.offsetHeight + r,
            l = this._currentZoom;
        (l === 1 / 0 || isNaN(l)) && (l = 1); var h = this.options.enforceBoundary ? 0 : Number.NEGATIVE_INFINITY; return i = Math.max(h, i / l), n = Math.max(h, n / l), a = Math.max(h, a / l), s = Math.max(h, s / l), { points: [j(i), j(n), j(a), j(s)], zoom: l, orientation: this.data.orientation }
    } var N = { type: "canvas", format: "png", quality: 1 },
        S = ["jpeg", "webp", "png"];

    function P(e) {
        var t = this,
            i = H.call(t),
            n = h(u(N), u(e)),
            o = "string" == typeof e ? e : n.type || "base64",
            r = n.size || "viewport",
            a = n.format,
            s = n.quality,
            l = n.backgroundColor,
            c = "boolean" == typeof n.circle ? n.circle : "circle" === t.options.viewport.type,
            m = t.elements.viewport.getBoundingClientRect(),
            f = m.width / m.height; return "viewport" === r ? (i.outputWidth = m.width, i.outputHeight = m.height) : "object" == typeof r && (r.width && r.height ? (i.outputWidth = r.width, i.outputHeight = r.height) : r.width ? (i.outputWidth = r.width, i.outputHeight = r.width / f) : r.height && (i.outputWidth = r.height * f, i.outputHeight = r.height)), S.indexOf(a) > -1 && (i.format = "image/" + a, i.quality = s), i.circle = c, i.url = t.data.url, i.backgroundColor = l, new Promise(function (e, n) {
                switch (o.toLowerCase()) {
                    case "rawcanvas":
                        e(A.call(t, i)); break;
                    case "canvas":
                    case "base64":
                        e(function (e) { return A.call(this, e).toDataURL(e.format, e.quality) }.call(t, i)); break;
                    case "blob":
                        (function (e) { var t = this; return new Promise(function (i, n) { A.call(t, e).toBlob(function (e) { i(e) }, e.format, e.quality) }) }).call(t, i).then(e); break;
                    default:
                        e(function (e) {
                            var t = e.points,
                                i = document.createElement("div"),
                                n = document.createElement("img"),
                                o = t[2] - t[0],
                                r = t[3] - t[1]; return d(i, "croppie-result"), i.appendChild(n), p(n, { left: -1 * t[0] + "px", top: -1 * t[1] + "px" }), n.src = e.url, p(i, { width: o + "px", height: r + "px" }), i
                        }.call(t, i))
                }
            })
    }

    function D(e) {
        if (!this.options.useCanvas || !this.options.enableOrientation) throw "Croppie: Cannot rotate without enableOrientation && EXIF.js included"; var t, i, n, o, r, l = this.elements.canvas;
        this.data.orientation = (t = this.data.orientation, i = e, n = a.indexOf(t) > -1 ? a : s, o = n.indexOf(t), r = i / 90 % n.length, n[(n.length + o + r % n.length) % n.length]), x(l, this.elements.img, this.data.orientation), k.call(this), _.call(this), copy = null
    } if (window.jQuery) {
        var T = window.jQuery;
        T.fn.croppie = function (e) {
            if ("string" === typeof e) {
                var t = Array.prototype.slice.call(arguments, 1),
                    i = T(this).data("croppie"); return "get" === e ? i.get() : "result" === e ? i.result.apply(i, t) : "bind" === e ? i.bind.apply(i, t) : this.each(function () {
                        var i = T(this).data("croppie"); if (i) {
                            var n = i[e]; if (!T.isFunction(n)) throw "Croppie " + e + " method not found";
                            n.apply(i, t), "destroy" === e && T(this).removeData("croppie")
                        }
                    })
            } return this.each(function () {
                var t = new q(this, e);
                t.$ = T, T(this).data("croppie", t)
            })
        }
    }

    function q(e, t) {
        if (e.className.indexOf("croppie-container") > -1) throw new Error("Croppie: Can't initialize croppie more than once"); if (this.element = e, this.options = h(u(q.defaults), t), "img" === this.element.tagName.toLowerCase()) {
            var i = this.element;
            d(i, "cr-original-image"), m(i, { "aria-hidden": "true", alt: "" }); var n = document.createElement("div");
            this.element.parentNode.appendChild(n), n.appendChild(i), this.element = n, this.options.url = this.options.url || i.src
        } if (C.call(this), this.options.url) {
            var o = { url: this.options.url, points: this.options.points };
            delete this.options.url, delete this.options.points, O.call(this, o)
        }
    }
    q.defaults = { viewport: { width: 100, height: 100, type: "square" }, boundary: {}, orientationControls: { enabled: !0, leftClass: "", rightClass: "" }, resizeControls: { width: !0, height: !0 }, customClass: "", showZoomer: !0, enableZoom: !0, enableResize: !1, mouseWheelZoom: !0, enableExif: !1, enforceBoundary: !0, enableOrientation: !1, enableKeyMovement: !0, update: function () { } }, q.globals = { translate: "translate3d" }, h(q.prototype, {
        bind: function (e, t) { return O.call(this, e, t) }, get: function () {
            var e = H.call(this),
                t = e.points; return this.options.relative && (t[0] /= this.elements.img.naturalWidth / 100, t[1] /= this.elements.img.naturalHeight / 100, t[2] /= this.elements.img.naturalWidth / 100, t[3] /= this.elements.img.naturalHeight / 100), e
        }, result: function (e) { return P.call(this, e) }, refresh: function () { return function () { W.call(this) }.call(this) }, setZoom: function (e) { L.call(this, e), c(this.elements.zoomer) }, rotate: function (e) { D.call(this, e) }, destroy: function () {
            return function () {
                var e, t;
                this.element.removeChild(this.elements.boundary), e = this.element, t = "croppie-container", e.classList ? e.classList.remove(t) : e.className = e.className.replace(t, ""), this.options.enableZoom && this.element.removeChild(this.elements.zoomerWrap), delete this.elements
            }.call(this)
        }
    }), e.Croppie = window.Croppie = q
});

jQuery(document).ready(function ($) {

    $(window).load(function () {
        // Animate loader off screen
        $(".loader").hide();
    });


    /* ------------- fidback ----------------- */
    // document.addEventListener('DOMContentLoaded', () => {
    //     function sendMessages(input1, input2) {
    //         jQuery(".button-fidback").prop("disabled", true);
    //         jQuery('.loader-request').css('display', 'block');
    //         var part1 = jQuery('#' + input1).val();
    //         var part2 = jQuery('#' + input2).val();

    //         if ((part1.length > 0) && (part2.length > 0)) {
    //             jQuery.ajax({
    //                 url: "{% url 'message:send_message_error' %}",
    //                 method: 'POST',
    //                 data: { title_support: part1, content_support: part2 },
    //                 success: function () {
    //                     var elements = jQuery('.support-overlay, .support');
    //                     jQuery(".button-fidback").prop("disabled", false);
    //                     elements.removeClass('actives');
    //                     jQuery('#' + input1).val('');
    //                     jQuery('#' + input2).val('');
    //                     //  jQuery( ".input-send" ).prop( "disabled", true );
    //                     jQuery('.loader-request').css('display', 'none');
    //                     var x = document.getElementById('toast1');
    //                     x.className = "show";
    //                     setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
    //                     setTimeout(function () { location.reload(); }, 4000);
    //                 }
    //             }).error(function () {
    //                 //   jQuery( ".input-send" ).prop( "disabled", true );
    //                 jQuery(".button-fidback").prop("disabled", false);
    //                 jQuery('.loader-request').css('display', 'none');
    //                 var x = document.getElementById("toast-err1");
    //                 x.className = "show";
    //                 setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
    //                 setTimeout(function () { location.reload(); }, 4000);
    //             })
    //         } else {
    //             jQuery(".button-fidback").prop("disabled", false);
    //             var x = document.getElementById("toast-not1");
    //             jQuery('.loader-request').css('display', 'none');
    //             x.className = "show";
    //             setTimeout(function () { x.className = x.className.replace("show", ""); }, 5000);
    //         }
    //     };

    // })
    /* ------------- Crop Images ----------------- */
    jQuery(document).ready(function ($) {
        var uploadCrop;
        $("#avatarbox").click(function () {
            $("#avatar").click();
        })
        uploadCrop = $('#imgs').croppie({
            viewport: {
                width: 200,
                height: 200,
            },
        });

        function readFileAvatar(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    uploadCrop.croppie('bind', {
                        url: e.target.result
                    });
                }
                reader.readAsDataURL(input.files[0]);
            } else {
                swal("Sorry - you're browser doesn't support the FileReader API");
            }
        }
        $('#avatar').on('change', function () {
            readFileAvatar(this);
            $('.popup-frame').fadeIn();
        });

        $('#crop').on('click', function (ev) {
            uploadCrop.croppie('result', {
                type: 'base64',
                format: 'jpeg',
                size: {
                    width: 600,
                    height: 600
                }
            }).then(function (resp) {
                $('.img-avatar').attr('src', resp);
                $(".avatar-base64").val(resp);
                $("#avatar").prop('required', false).val("");
                $('.popup-frame').fadeOut();
            });
        });
        $('.msg-text img,.closeicon').click(function () {
            $(this).parent().parent().fadeOut();
        });
    });

    /*------------- startup --------------- */

    $(".cat-shetab:checked").each(function () {
        $(".hiderahbar").toggle();
    })
    if ($(".cat-shetab:checked")) {

    } else {

    }
    $(".cat-shetab").change(function () {
        if ($(".cat-shetab:checked")) {
            $(".hiderahbar").toggle();
            $(".val").val("");
            $('.removing').remove();
            $('#mentor-id').prop('disabled', false);
        }
        if (!$(".cat-shetab").is(':checked')) {

            $(".val-shetab").val("");
        }

    });



    $(".add-team").on("click", function () {
        if ($('.group').length < 10) {
            $('.clone').clone().addClass('group').removeClass('clone hide').insertBefore('.clone');
        }
    })

    // var uri = window.location.toString();
    // if (uri.indexOf("?") > 0) {
    //     var clean_uri = uri.substring(0, uri.indexOf("?"));
    //     window.history.replaceState({}, document.title, clean_uri);
    // }
    $('.check-error').blur(function () {
        var thisInput = $(this);
        var dataValue = thisInput.val();
        var dataType = thisInput.data('type');
        $.ajax({
            url: '',
            method: 'POST',
            data: {
                type: dataType,
                value: dataValue
            },
            success: function (response) {
                var error = $(response).filter('.notify').text();
                var errorArr = ['error_email'];
                if ($.inArray(error, errorArr) !== -1) {
                    $('#' + error).show();
                    thisInput.val('');
                } else $('.error-hide').hide();

            }
        })
    });


    Dropzone.prototype.defaultOptions.dictFallbackMessage = "مرورگر شما آپلود فایل drag'n'drop را پشتیبانی نمی کند.";
    Dropzone.prototype.defaultOptions.dictFallbackText = "Please use the fallback form below to upload your files like in the olden days.";
    Dropzone.prototype.defaultOptions.dictFileTooBig = "فایل خیلی بزرگ است ({{filesize}}MB)  حداکثر اندازه فایل: {{maxFilesize}}MB";
    Dropzone.prototype.defaultOptions.dictInvalidFileType = "شما مجاز به بارگذاری این نوع فایل نیستید";
    Dropzone.prototype.defaultOptions.dictResponseError = "Server responded with {{statusCode}} code.";
    Dropzone.prototype.defaultOptions.dictCancelUpload = "انصراف از بارگذاری";
    Dropzone.prototype.defaultOptions.dictCancelUploadConfirmation = "آیا مطمئن هستید که میخواهید این بارگذاری را لغو کنید؟";
    Dropzone.prototype.defaultOptions.dictRemoveFile = "حذف فایل";
    Dropzone.prototype.defaultOptions.dictRemoveFileConfirmation = null;
    Dropzone.prototype.defaultOptions.dictMaxFilesExceeded = "شما فقط می توانید {{maxFiles}} فایل بارگذاری کنید  .";
    Dropzone.prototype.defaultOptions.dictDefaultMessage = "برای بارگذاری فایل کلیک کنید";
    Dropzone.options.uploadVideo = {
        autoProcessQueue: true,
        timeout: 1800000,
        maxFiles: 1,
        maxFilesize: 40, // MB
        paramName: "video",
        addRemoveLinks: true,
        acceptedFiles: '.mp4,.mkv,.avi,.mov,.wmv',
        init: function () {
            var self = this;
            this.on("success", function (file, responseText) {
                console.log(responseText);
            });
            this.on('error', function (file, response) {
                $('.text-error').text(response);
                $('.message-alert').fadeIn();
                $('.message-alert').delay(4000).fadeOut();
            });
            self.on("maxfilesexceeded", function (file) {
                self.removeAllFiles();
                self.addFile(file);
            });
            $("#send-video").click(function (e) {
                e.preventDefault();
                self.processQueue();
            });
            self.options.dictRemoveFile = "حذف";
            self.on("addedfile", function (file) {

            });
            self.on("removedfile", function (file) {

            });
        }
    }
    document.querySelectorAll('.toggle-element').forEach(element => {
        element.addEventListener('DOMSubtreeModified', () => {
            const toggle1 = element.querySelector('[data-type="toggle-1"]');
            if (toggle1) {
                const toggleButton = toggle1.querySelector('[data-type="toggle-btn"]');
                toggleButton.addEventListener('click', function () {
                    toggle1.classList.add('hide');
                    toggle2.classList.remove('hide');
                });
            }
            const toggle2 = element.querySelector('[data-type="toggle-2"]');


        });
    });
    /*------------- LightBox --------------- */


    $(".sg-tab").click(function () {
        $tab_num = $(this).data("id");
        if ($(this).hasClass("activee")) { } else {
            $(".sg-tab").removeClass("activee");
            $(this).addClass("activee");
            $(".sg-content").hide();
            $(".cnt" + $tab_num).fadeIn();
        }
    });


    $('.province').each(function () {
        var $province = $(this).data('value');
        var $city = $('.city').data('value');
        if ($province) {
            $('.province option[value=' + $province + ']').attr('selected', 'selected');
            $('.city').addClass("tempclass");
            loadCity($province);
            $('.city option[value=' + $city + ']').attr('selected', 'selected');
        }
    });






    jQuery(document).ready(function ($) {

        if($("p").hasClass("validation-errors")){       
            var valerr= $(".validation-errors");
            var errorval= $(".validation-errors").html();
            var placeerror=$("#get-errors");
            placeerror.html(errorval);
            valerr.remove();
          }



        var elements = $('.support-overlay, .support');

        $('.btn-support').click(function () {
            elements.addClass('actives');
        });

        $('.close-support').click(function () {
            elements.removeClass('actives');
        });

    });


    /*---------- textarea characters ---------- */
    function setCharCountListener() {
        document.querySelectorAll(".char-count").forEach(element => {
            const textArea = element.querySelector("textarea");
            const holder = element.querySelector("p");
            const maxlength = textArea.getAttribute("maxlength");

            textArea.addEventListener("input", event => {
                holder.innerText = `${event.target.value.length}/${maxlength}`;
            });
            holder.innerText = `0/${maxlength}`;
        });
    }
    setCharCountListener();
    /*------------- ScrollToTop --------------- */
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $(".scrollToTop").fadeIn();
        } else {
            $(".scrollToTop").fadeOut();
        }
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 125) {
            $(".susu").addClass("fixed");
            $(".susu").addClass("fixed-sidebar-left");
        } else {
            $(".susu").removeClass("fixed");
            $(".susu").removeClass("fixed-sidebar-left");
        }
    });
    $(".scrollToTop").click(function () {
        $("html, body").animate({
            scrollTop: 0
        },
            800
        );
        return false;
    });
    $("#cssmenu li.active")
        .addClass("open")
        .children("ul")
        .show();
    $("#cssmenu li.has-sub>a").on("click", function () {
        $(this).removeAttr("href");
        var element = $(this).parent("li");
        if (element.hasClass("open")) {
            element.removeClass("open");
            element.find("li").removeClass("open");
            element.find("ul").slideUp(200);
        } else {
            element.addClass("open");
            element.children("ul").slideDown(200);
            element
                .siblings("li")
                .children("ul")
                .slideUp(200);
            element.siblings("li").removeClass("open");
            element
                .siblings("li")
                .find("li")
                .removeClass("open");
            element
                .siblings("li")
                .find("ul")
                .slideUp(200);
        }
    });

    $(".close-toggle").click(function () {
        $(".menu-admin").css("width", "0px");
        $(".box-admin").css("padding-right", "10px");
        $(".close-toggle").addClass("open-toggle");
        $(".close-toggle").removeClass();
        $(".menu-admin").fadeOut(250);
    });

    $(".avatar-user").click(function () {
        $(".dropd").fadeToggle(500);
        $(".dropdlang").fadeToggle(500);
    });
    /*------------- MobileMenu --------------- */
    $(".header-right-mob").click(function () {
        $(".mob-swipe-bg").show();
        value1 = $(".mobile-menu-right").css("right") === "-260px" ? 0 : "-260px";
        $(".mobile-menu-right")
            .stop()
            .css({
                right: value1
            });
    });
    $(".mob-swipe-bg").click(function () {
        $(".mob-swipe-bg").hide();
        $(".mobile-menu-right").css("right", "-260px");
    });
    $(".header-search-mob").click(function () {
        $(".mobile-search").show("slow");
        $(".mobile-search-input").focus();
    });
    $(".search-close").click(function () {
        $(".mobile-search").hide("slow");
    });

    var maxLength = 280;
    $("#team-excerpt").keyup(function () {
        var length = $(this).val().length;
        var length = maxLength - length;
        $(".text-counter").text(length);
    });
    $("#team-excerpt1").keyup(function () {
        var length = $(this).val().length;
        var length = maxLength - length;
        $(".text-counter1").text(length);
    });
    $("#team-excerpt2").keyup(function () {
        var length = $(this).val().length;
        var length = maxLength - length;
        $(".text-counter2").text(length);
    });


    $("form").submit(function () {
        $form = $("form");
        if ($(".smart-validate").valid()) {
            $(".loader").fadeIn();
        }
    });

    /* ---------Ajax ------------*/




    /* ---------- aleart  -----------*/
    var fademessage = $(".message-producer")
        .delay(3500)
        .fadeOut();

    /* ---------- step  -----------*/
    $(".step").each(function (index, el) {
        $(el)
            .not(".active")
            .addClass("done");
        $(".done").html('<i class="icon-valid"></i>');
        if ($(this).is(".active")) {
            $(this)
                .parent()
                .addClass("pulse");
            return false;
        }
    });


    $(document).on("focus", ".datepicker", function () {
        $(".datepicker").persianDatepicker({
            format: "YYYY/MM/DD",
            initialValue: false,
            altField: ".datepicker-alt",
        });

    });
    $(".datepicker-gregorian").persianDatepicker({
        viewMode: 'year',
        initialValueType: 'gregorian',
        format: "YYYY/MM/DD",
        initialValueType: 'persian'
    });
    $(".log-date").persianDatepicker({
        altField: '#observer',
        initialValue: false,
        altFormat: "X",
        observer: true,
        format: 'YYYY/MM/DD',
        initialValueType: 'persian',
        timePicker: {
            enabled: true
        },
    });
    $(".log-date1").persianDatepicker({
        altField: '#observer1',
        altFormat: "X",
        initialValue: false,
        observer: true,
        format: 'YYYY/MM/DD',
        initialValueType: 'persian',
        timePicker: {
            enabled: true
        },
    });
    $("#start-date").persianDatepicker({
        format: "YYYY/MM/DD",
        initialValue: false,
        maxDate: new persianDate(),
        initialValueType: 'persian'
    });
    var i;
    for (i = 0; i < 8; i++) {
        $(".start-date" + i).persianDatepicker({
            format: "YYYY-MM-DD",
            altField: '.observer-start-date-alt' + i
        });
        $('.timepicker-s' + i).persianDatepicker({
            onlyTimePicker: true,
            format: "H:m",
            initialValue: false,

            observer: true,
            altField: '.observer-timepicker-s-alt' + i
        });

        $('.timepicker-e' + i).persianDatepicker({
            onlyTimePicker: true,
            format: "H:m",
            initialValue: false,

            observer: true,
            altField: '.observer-timepicker-e-alt' + i
        });
    }


    $('.timepicker-s').persianDatepicker({
        onlyTimePicker: true,
        format: "H:m",
        initialValue: true,
        altField: '.observer-timepicker-s-alt'
    });

    $('.timepicker-e').persianDatepicker({
        onlyTimePicker: true,
        format: "H:m",
        initialValue: true,
        altField: '.observer-timepicker-e-alt'
    });




    $(".showhide").change(function () {
        $show_id = $(this).data("show-id");
        $(".hidden").hide();
        if ($(this).is(":checked")) {
            $("#" + $show_id).show();
        }
    });
    $(".showhide").each(function () {
        $show_id = $(this).data("show-id");
        if ($(this).is(":checked")) {
            $("#" + $show_id).show();
        }
    });
});


/* ---------- messages  -----------*/


/* ---------- search roles  -----------*/
function searchApi(id, resultId, name, path = null, companion) {

    var searchRequest = null;
    var resultid = resultId;
    var _resultid = "'" + resultId + "'";
    var param = name;
    var _id = '.' + id;
    var minlength = 2;
    var refereeAPI = "/api/?";
    var res = document.getElementById(resultid);
    styleResult = 'searchresult';
    if (path == 'startup') styleResult = 'searchresult2';
    if (name == 'investor') styleResult = 'searchresult3';

    clearTimeout(this.delay);
    this.delay = setTimeout(function () {
        var field, that = this,
            value = jQuery(_id).val();

        if (value.length >= minlength) {
            jQuery(".start-load").show();
            console.log("test-12");
            args = {
                type: param,
                fields: value,
                companion: companion
            };
            jQuery.getJSON(refereeAPI, args).done(function (data) {
                res.innerHTML = "";
                if (data.length) {
                    jQuery(".start-load").hide();
                    var output = '<ul class="' + styleResult + '">';
                    jQuery.each(data, function (i, item) {
                        output += '<li  data-id="' + item.id + '" data-name="' + item.name + '">';
                        output += '<span>' + item.name + '</span>';
                        output += '</li>';
                        if (i === 8) {
                            return false;
                        }
                    });
                    output += '</ul>';
                    res.style.display = "block";
                    res.innerHTML = output;
                    res.firstElementChild.style.display = "block";

                    // jQuery(that).closest('.'+resultId).append(output);
                } else {
                    // jQuery(that).closest('.'+resultId).append('<span class="font-s14">ŁŲ±ŲÆŪ ŲØŲ§ Ų§ŪŁ† Ł†Ų§Ł… Ł¾ŪŲÆŲ§ Ł†Ų´ŲÆ</span>');
                    jQuery(".start-load").hide();
                    var output = '<ul class="' + styleResult + '">';
                    output += '<li>';
                    output += '<span class="font-s14">فردی با این نام پیدا نشد</span>';
                    output += '</li>';
                    if (path == 'startup') {
                        output += '<li>';
                        output += '<span class="font-s14 create-leader btn-web align-center margin-auto spacer-r38"><i class="fa fa-plus-circle font-s10 pad-l10"></i>افزودن راهبر جدید</span>';
                        output += '</li>';
                    }
                    res.style.display = "block";
                    res.innerHTML = output;
                    res.firstElementChild.style.display = "block";
                }
            }).fail(function () {
                console.log("error");
            }).always(function () {

            });
        } else {
            res.innerHTML = "";
            // res.style.display = "none";
            // jQuery(that).siblings('.'+resultid).html('').hide();
        }
    }.bind(this), 500);

    jQuery(document).on('click', '#' + resultid + ' .' + styleResult + ' li', function ($) {
        var id = jQuery(this).data("id");
        var name = jQuery(this).data("name");
        jQuery(this).parents().eq(2).find('.choosen-name').val(name);
        jQuery(this).parents().eq(2).find('.choosen-id').val(id).trigger('change');
        res.style.display = "none";
    })
    document.querySelectorAll('.back-button')
        .forEach(element => 
            element.addEventListener('click', () => {
                window.history.back();
            }
    ));
}