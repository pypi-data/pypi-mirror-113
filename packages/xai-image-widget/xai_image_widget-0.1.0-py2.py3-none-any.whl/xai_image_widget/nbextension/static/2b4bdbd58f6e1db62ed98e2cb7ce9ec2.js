(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./$$_lazy_route_resource lazy recursive":
/*!******************************************************!*\
  !*** ./$$_lazy_route_resource lazy namespace object ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(function() {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "./$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "./src/app/app.ts":
/*!************************!*\
  !*** ./src/app/app.ts ***!
  \************************/
/*! exports provided: App */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "App", function() { return App; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _img_feature_attr_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../img_feature_attr/img_feature_attr_viz */ "./src/img_feature_attr/img_feature_attr_viz.ts");
/* harmony import */ var _img_feature_attr_attr_histogram__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../img_feature_attr/attr_histogram */ "./src/img_feature_attr/attr_histogram.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");





/**
 * The root component.
 */
var App = /** @class */ (function () {
    function App() {
        this.title = 'xai_widgets';
    }
    App.ɵfac = function App_Factory(t) { return new (t || App)(); };
    App.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({ type: App, selectors: [["app-root"]], decls: 5, vars: 0, consts: [[1, "inline", "attr-component"]], template: function App_Template(rf, ctx) { if (rf & 1) {
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](1, "app-img-feature-attr-viz");
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 0);
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](3, "app-attr-histogram");
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](4, "router-outlet");
        } }, directives: [_img_feature_attr_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_1__["ImgFeatureAttrViz"], _img_feature_attr_attr_histogram__WEBPACK_IMPORTED_MODULE_2__["AttrHistogram"], _angular_router__WEBPACK_IMPORTED_MODULE_3__["RouterOutlet"]], styles: [".attr-component[_ngcontent-%COMP%] {\n  vertical-align: top;\n  margin-right: 2em;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi90bXAveGFpX2ltYWdlX3dpZGdldC94YWlfaW1hZ2Vfd2lkZ2V0L3dlYmFwcC9zcmMvYXBwL2FwcC5zY3NzIiwic3JjL2FwcC9hcHAuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFDQTtFQUNFLG1CQUFBO0VBQ0EsaUJBQUE7QUNBRiIsImZpbGUiOiJzcmMvYXBwL2FwcC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiXG4uYXR0ci1jb21wb25lbnR7XG4gIHZlcnRpY2FsLWFsaWduOnRvcDtcbiAgbWFyZ2luLXJpZ2h0OiAyZW07XG59XG4iLCIuYXR0ci1jb21wb25lbnQge1xuICB2ZXJ0aWNhbC1hbGlnbjogdG9wO1xuICBtYXJnaW4tcmlnaHQ6IDJlbTtcbn0iXX0= */"] });
    return App;
}());

/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](App, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
                selector: 'app-root',
                templateUrl: './app.ng.html',
                styleUrls: ['./app.scss']
            }]
    }], null, null); })();


/***/ }),

/***/ "./src/app/app_module.ts":
/*!*******************************!*\
  !*** ./src/app/app_module.ts ***!
  \*******************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser/animations */ "./node_modules/@angular/platform-browser/__ivy_ngcc__/fesm5/animations.js");
/* harmony import */ var _img_feature_attr_img_feature_attr_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../img_feature_attr/img_feature_attr_module */ "./src/img_feature_attr/img_feature_attr_module.ts");
/* harmony import */ var _app__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app */ "./src/app/app.ts");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./app_routing_module */ "./src/app/app_routing_module.ts");






/**
 * The main application module.
 */
var AppModule = /** @class */ (function () {
    function AppModule() {
    }
    AppModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({ type: AppModule, bootstrap: [_app__WEBPACK_IMPORTED_MODULE_3__["App"]] });
    AppModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({ factory: function AppModule_Factory(t) { return new (t || AppModule)(); }, providers: [], imports: [[
                _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__["BrowserAnimationsModule"],
                _app_routing_module__WEBPACK_IMPORTED_MODULE_4__["AppRoutingModule"],
                _img_feature_attr_img_feature_attr_module__WEBPACK_IMPORTED_MODULE_2__["ImgFeatureAttrModule"],
            ]] });
    return AppModule;
}());

(function () { (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](AppModule, { declarations: [_app__WEBPACK_IMPORTED_MODULE_3__["App"]], imports: [_angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__["BrowserAnimationsModule"],
        _app_routing_module__WEBPACK_IMPORTED_MODULE_4__["AppRoutingModule"],
        _img_feature_attr_img_feature_attr_module__WEBPACK_IMPORTED_MODULE_2__["ImgFeatureAttrModule"]] }); })();
/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](AppModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{
                declarations: [
                    _app__WEBPACK_IMPORTED_MODULE_3__["App"],
                ],
                imports: [
                    _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__["BrowserAnimationsModule"],
                    _app_routing_module__WEBPACK_IMPORTED_MODULE_4__["AppRoutingModule"],
                    _img_feature_attr_img_feature_attr_module__WEBPACK_IMPORTED_MODULE_2__["ImgFeatureAttrModule"],
                ],
                providers: [],
                bootstrap: [_app__WEBPACK_IMPORTED_MODULE_3__["App"]]
            }]
    }], null, null); })();


/***/ }),

/***/ "./src/app/app_routing_module.ts":
/*!***************************************!*\
  !*** ./src/app/app_routing_module.ts ***!
  \***************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/__ivy_ngcc__/fesm5/router.js");




var routes = [];
var AppRoutingModule = /** @class */ (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineNgModule"]({ type: AppRoutingModule });
    AppRoutingModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineInjector"]({ factory: function AppRoutingModule_Factory(t) { return new (t || AppRoutingModule)(); }, imports: [[_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forRoot(routes)], _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]] });
    return AppRoutingModule;
}());

(function () { (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵsetNgModuleScope"](AppRoutingModule, { imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]], exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]] }); })();
/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](AppRoutingModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"],
        args: [{ imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forRoot(routes)], exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]] }]
    }], null, null); })();


/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
/**
 * @fileoverview Configure the environment to be non-production.
 *
 * This is used in non-Google3 environment only.
 */
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
var environment = {
    production: false
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`,
 * `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a
 * negative impact on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/img_feature_attr/attr_histogram.ts":
/*!************************************************!*\
  !*** ./src/img_feature_attr/attr_histogram.ts ***!
  \************************************************/
/*! exports provided: AttrHistogram */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AttrHistogram", function() { return AttrHistogram; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! d3 */ "./node_modules/d3/index.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _feature_attr_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./feature_attr_service */ "./src/img_feature_attr/feature_attr_service.ts");







var _c0 = ["attr_histogram"];
// Constants for max/min attribution values shown in the histogram
var MIN_ATTR_VAL = -1;
var MAX_ATTR_VAL = 1;
/**
 * AttrHistogram: a component for showing the histogram of attribution
 * values. Each bar represents a segment of attribution values, and its
 * height represents the number of pixels that have attribution values
 * within that range segment.
 */
var AttrHistogram = /** @class */ (function () {
    function AttrHistogram(featureAttrService) {
        this.featureAttrService = featureAttrService;
        this.imgAttrVector = this.featureAttrService.imgAttrVectorSource;
        this.barWidth = 20;
        this.width = 300;
        this.height = 100;
        this.margin = { left: 30, top: 15, bottom: 50, right: 30 };
        this.textLoc = this.barWidth / 2;
        this.currentRange = [MIN_ATTR_VAL, MAX_ATTR_VAL];
        // Handle on-destroy Subject, used to unsubscribe.
        this.destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_2__["ReplaySubject"](1);
    }
    AttrHistogram.prototype.ngAfterViewInit = function () {
        var _this = this;
        this.imgAttrVector.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(this.destroyed))
            .subscribe(function (data) {
            if (_this.attrHistSvg) {
                // reset the range every time new data comes in
                _this.resetRange();
                // draw histogram
                _this.drawHistogram(_this.attrHistSvg, data);
            }
        });
    };
    AttrHistogram.prototype.ngOnDestroy = function () {
        // Unsubscribes all pending subscriptions.
        this.destroyed.next();
        this.destroyed.complete();
    };
    /**
     * Reset current range to [-1.0, 1.0];
     */
    AttrHistogram.prototype.resetRange = function () {
        this.currentRange = [MIN_ATTR_VAL, MAX_ATTR_VAL];
    };
    /**
     * The main function for drawing the histogram onto the SVG
     * element.
     */
    AttrHistogram.prototype.drawHistogram = function (targetEle, data) {
        if (!targetEle) {
            throw new Error('undefined target for visualization');
        }
        else {
            var g = this.getAdjustedSVGGElement(targetEle);
            // filter to non-zero data points
            var nonZeroData = data.filter(function (ele) { return ele !== 0; });
            // get xScale and xDomains
            var xScale = this.getXScale(nonZeroData);
            var bins = this.getBins(xScale, nonZeroData);
            var yScale = this.getYScale(bins);
            this.addBars(g, xScale, yScale, bins);
            this.addXAxis(g, xScale);
        }
    };
    /**
     * Adjust the size of the SVG and adjust margins via
     * g element transform. Then return the selection of SVGGElement.
     */
    AttrHistogram.prototype.getAdjustedSVGGElement = function (targetEle) {
        var ele = targetEle.nativeElement;
        var selectedEle = d3__WEBPACK_IMPORTED_MODULE_1__["select"](ele);
        selectedEle.style('width', this.width + this.margin.left + this.margin.right);
        selectedEle.style('height', this.height + this.margin.top + this.margin.bottom);
        var g = selectedEle.select('g');
        // set margin
        g.attr('transform', "translate(" + this.margin.left + ", " + this.margin.top + ")");
        return g;
    };
    /**
     * Given the non-zero dataset, return the scale of x axis.
     */
    AttrHistogram.prototype.getXScale = function (nonZeroData) {
        var xMin = d3__WEBPACK_IMPORTED_MODULE_1__["min"](nonZeroData);
        var xMax = d3__WEBPACK_IMPORTED_MODULE_1__["max"](nonZeroData);
        var xScale = d3__WEBPACK_IMPORTED_MODULE_1__["scaleLinear"]().domain([xMin, xMax]).nice().rangeRound([
            0, this.width
        ]);
        return xScale;
    };
    /**
     * Given the x scale and the non-zero dataset, return the bins
     * for histogram.
     */
    AttrHistogram.prototype.getBins = function (xScale, nonZeroData) {
        var xDomain = xScale.domain();
        // bin generators
        var generator = d3__WEBPACK_IMPORTED_MODULE_1__["histogram"]()
            .domain([xDomain[0], xDomain[1]])
            .thresholds(xScale.ticks(10));
        var bins = generator(nonZeroData);
        return bins;
    };
    /**
     * Given the histogram bins, return the y axis scale.
     */
    AttrHistogram.prototype.getYScale = function (bins) {
        var yScale = d3__WEBPACK_IMPORTED_MODULE_1__["scaleLinear"]()
            .domain([
            0,
            d3__WEBPACK_IMPORTED_MODULE_1__["max"](bins, function (bin) {
                return bin.length;
            })
        ])
            .nice()
            .range([this.height, 0]);
        return yScale;
    };
    /**
     * Given selected g element, xScale, yScale and bins, add histogram
     * bars to the g element.
     */
    AttrHistogram.prototype.addBars = function (g, xScale, yScale, bins) {
        var _this = this;
        var formatCount = d3__WEBPACK_IMPORTED_MODULE_1__["format"](',.0f');
        // appending the histogram bars
        var bar = g.selectAll('.bar')
            .data(bins)
            .enter()
            .append('g')
            .attr('class', 'bar')
            .attr('transform', function (bin) {
            var x0 = bin.x0;
            return "translate(" + xScale(x0) + ", " + yScale(bin.length) + ")";
        });
        bar.append('rect')
            .attr('x', 1)
            .attr('width', this.barWidth)
            .attr('height', function (bin) {
            return _this.height - yScale(bin.length);
        });
        bar.append('text')
            .attr('dy', '.75em')
            .attr('y', -10)
            .attr('x', this.textLoc)
            .attr('text-anchor', 'middle')
            .text(function (bin) {
            return formatCount(bin.length);
        });
    };
    /**
     * Given selected g element and xScale, add the xAxis (including
     * the ticks and label) to the g element.
     */
    AttrHistogram.prototype.addXAxis = function (g, xScale) {
        // remove existing x axis
        g.select('g.x-axis').remove();
        // append a new x axis
        var xaxis = g.append('g')
            .attr('class', 'axis x-axis')
            .attr('transform', "translate(0, " + this.height + ")")
            .call(d3__WEBPACK_IMPORTED_MODULE_1__["axisBottom"](xScale));
        xaxis.append('text')
            .attr('class', 'axis-label')
            .attr('transform', "translate(" + this.width / 2 + ", " + this.margin.bottom / 2 + ")")
            .style('text-anchor', 'middle')
            .text('Attribution Values');
    };
    AttrHistogram.ɵfac = function AttrHistogram_Factory(t) { return new (t || AttrHistogram)(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdirectiveInject"](_feature_attr_service__WEBPACK_IMPORTED_MODULE_4__["FeatureAttrService"])); };
    AttrHistogram.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵdefineComponent"]({ type: AttrHistogram, selectors: [["app-attr-histogram"]], viewQuery: function AttrHistogram_Query(rf, ctx) { if (rf & 1) {
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵviewQuery"](_c0, true);
        } if (rf & 2) {
            var _t;
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵloadQuery"]()) && (ctx.attrHistSvg = _t.first);
        } }, decls: 7, vars: 0, consts: [[1, "block-title"], [1, "description"], ["attr_histogram", ""]], template: function AttrHistogram_Template(rf, ctx) { if (rf & 1) {
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](0, "div", 0);
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](1, " Histogram of Pixel Attributions\n");
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](2, "div", 1);
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵtext"](3, " Bar height indicates the number of pixels with corresponding attribution values.\n");
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵnamespaceSVG"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementStart"](4, "svg", null, 2);
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelement"](6, "g");
            _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵɵelementEnd"]();
        } }, styles: [".block-title[_ngcontent-%COMP%] {\n  font-weight: 600;\n}\n\n.discription[_ngcontent-%COMP%] {\n  font-size: 10px;\n  color: \"#ccc\";\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi90bXAveGFpX2ltYWdlX3dpZGdldC94YWlfaW1hZ2Vfd2lkZ2V0L3dlYmFwcC9zcmMvaW1nX2ZlYXR1cmVfYXR0ci9pbWdfZmVhdHVyZV9hdHRyX3NoYXJlZF9zdHlsZS5zY3NzIiwic3JjL2ltZ19mZWF0dXJlX2F0dHIvaW1nX2ZlYXR1cmVfYXR0cl9zaGFyZWRfc3R5bGUuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGdCQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0VBQ0EsYUFBQTtBQ0NGIiwiZmlsZSI6InNyYy9pbWdfZmVhdHVyZV9hdHRyL2ltZ19mZWF0dXJlX2F0dHJfc2hhcmVkX3N0eWxlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuYmxvY2stdGl0bGUge1xuICBmb250LXdlaWdodDogNjAwO1xufVxuXG4uZGlzY3JpcHRpb24ge1xuICBmb250LXNpemU6IDEwcHg7XG4gIGNvbG9yOiAnI2NjYyc7XG59XG4iLCIuYmxvY2stdGl0bGUge1xuICBmb250LXdlaWdodDogNjAwO1xufVxuXG4uZGlzY3JpcHRpb24ge1xuICBmb250LXNpemU6IDEwcHg7XG4gIGNvbG9yOiBcIiNjY2NcIjtcbn0iXX0= */", "[_nghost-%COMP%]     .bar rect {\n  fill: steelblue;\n}\n[_nghost-%COMP%]     .bar text {\n  fill: black;\n  font: 10px sans-serif;\n}\n[_nghost-%COMP%]     .axis .axis-label {\n  fill: black;\n}\n[_nghost-%COMP%]     .current-range {\n  color: steelblue;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi90bXAveGFpX2ltYWdlX3dpZGdldC94YWlfaW1hZ2Vfd2lkZ2V0L3dlYmFwcC9zcmMvaW1nX2ZlYXR1cmVfYXR0ci9hdHRyX2hpc3RvZ3JhbS5zY3NzIiwic3JjL2ltZ19mZWF0dXJlX2F0dHIvYXR0cl9oaXN0b2dyYW0uc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFFSTtFQUNFLGVBQUE7QUNETjtBRElJO0VBQ0UsV0FBQTtFQUNBLHFCQUFBO0FDRk47QURNSTtFQUNFLFdBQUE7QUNKTjtBRE9FO0VBQ0UsZ0JBQUE7QUNMSiIsImZpbGUiOiJzcmMvaW1nX2ZlYXR1cmVfYXR0ci9hdHRyX2hpc3RvZ3JhbS5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiOmhvc3QgOjpuZy1kZWVwIHtcbiAgLmJhciB7XG4gICAgcmVjdCB7XG4gICAgICBmaWxsOiBzdGVlbGJsdWU7XG4gICAgfVxuXG4gICAgdGV4dCB7XG4gICAgICBmaWxsOiBibGFjaztcbiAgICAgIGZvbnQ6IDEwcHggc2Fucy1zZXJpZjtcbiAgICAgIH1cbiAgfVxuICAuYXhpcyB7XG4gICAgLmF4aXMtbGFiZWwge1xuICAgICAgZmlsbDogYmxhY2s7XG4gICAgfVxuICB9XG4gIC5jdXJyZW50LXJhbmdlIHtcbiAgICBjb2xvcjogc3RlZWxibHVlO1xuICB9XG59XG4iLCI6aG9zdCA6Om5nLWRlZXAgLmJhciByZWN0IHtcbiAgZmlsbDogc3RlZWxibHVlO1xufVxuOmhvc3QgOjpuZy1kZWVwIC5iYXIgdGV4dCB7XG4gIGZpbGw6IGJsYWNrO1xuICBmb250OiAxMHB4IHNhbnMtc2VyaWY7XG59XG46aG9zdCA6Om5nLWRlZXAgLmF4aXMgLmF4aXMtbGFiZWwge1xuICBmaWxsOiBibGFjaztcbn1cbjpob3N0IDo6bmctZGVlcCAuY3VycmVudC1yYW5nZSB7XG4gIGNvbG9yOiBzdGVlbGJsdWU7XG59Il19 */"] });
    return AttrHistogram;
}());

/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_0__["ɵsetClassMetadata"](AttrHistogram, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"],
        args: [{
                selector: 'app-attr-histogram',
                templateUrl: './attr_histogram.ng.html',
                styleUrls: ['./img_feature_attr_shared_style.scss', './attr_histogram.scss']
            }]
    }], function () { return [{ type: _feature_attr_service__WEBPACK_IMPORTED_MODULE_4__["FeatureAttrService"] }]; }, { attrHistSvg: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"],
            args: ['attr_histogram']
        }] }); })();


/***/ }),

/***/ "./src/img_feature_attr/colors.ts":
/*!****************************************!*\
  !*** ./src/img_feature_attr/colors.ts ***!
  \****************************************/
/*! exports provided: colors */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "colors", function() { return colors; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/** @fileoverview Constants for colors. */
var _a;


/** A set of constants related to colors. */
// LINT.IfChange
var colors = {
    // Colormap for creating the attributions heatmap. Each colormap is a list of
    // 256
    // RGB pixel values. The lowest attribution value to be visualized maps to the
    // index 0 in the colormap, whereas the highest attribution value to be
    // visualized maps to index 255 in the colormap.
    RED_COLORMAP: [
        [0.0, 0.0, 0.0], [64.248046875, 0.0, 0.0],
        [128.49609375, 0.0, 0.0], [128.994140625, 0.0, 0.0],
        [129.4921875, 0.0, 0.0], [129.990234375, 0.0, 0.0],
        [130.48828125, 0.0, 0.0], [130.986328125, 0.0, 0.0],
        [131.484375, 0.0, 0.0], [131.982421875, 0.0, 0.0],
        [132.48046875, 0.0, 0.0], [132.978515625, 0.0, 0.0],
        [133.4765625, 0.0, 0.0], [133.974609375, 0.0, 0.0],
        [134.47265625, 0.0, 0.0], [134.970703125, 0.0, 0.0],
        [135.46875, 0.0, 0.0], [135.966796875, 0.0, 0.0],
        [136.46484375, 0.0, 0.0], [136.962890625, 0.0, 0.0],
        [137.4609375, 0.0, 0.0], [137.958984375, 0.0, 0.0],
        [138.45703125, 0.0, 0.0], [138.955078125, 0.0, 0.0],
        [139.453125, 0.0, 0.0], [139.951171875, 0.0, 0.0],
        [140.44921875, 0.0, 0.0], [140.947265625, 0.0, 0.0],
        [141.4453125, 0.0, 0.0], [141.943359375, 0.0, 0.0],
        [142.44140625, 0.0, 0.0], [142.939453125, 0.0, 0.0],
        [143.4375, 0.0, 0.0], [143.935546875, 0.0, 0.0],
        [144.43359375, 0.0, 0.0], [144.931640625, 0.0, 0.0],
        [145.4296875, 0.0, 0.0], [145.927734375, 0.0, 0.0],
        [146.42578125, 0.0, 0.0], [146.923828125, 0.0, 0.0],
        [147.421875, 0.0, 0.0], [147.919921875, 0.0, 0.0],
        [148.41796875, 0.0, 0.0], [148.916015625, 0.0, 0.0],
        [149.4140625, 0.0, 0.0], [149.912109375, 0.0, 0.0],
        [150.41015625, 0.0, 0.0], [150.908203125, 0.0, 0.0],
        [151.40625, 0.0, 0.0], [151.904296875, 0.0, 0.0],
        [152.40234375, 0.0, 0.0], [152.900390625, 0.0, 0.0],
        [153.3984375, 0.0, 0.0], [153.896484375, 0.0, 0.0],
        [154.39453125, 0.0, 0.0], [154.892578125, 0.0, 0.0],
        [155.390625, 0.0, 0.0], [155.888671875, 0.0, 0.0],
        [156.38671875, 0.0, 0.0], [156.884765625, 0.0, 0.0],
        [157.3828125, 0.0, 0.0], [157.880859375, 0.0, 0.0],
        [158.37890625, 0.0, 0.0], [158.876953125, 0.0, 0.0],
        [159.375, 0.0, 0.0], [159.873046875, 0.0, 0.0],
        [160.37109375, 0.0, 0.0], [160.869140625, 0.0, 0.0],
        [161.3671875, 0.0, 0.0], [161.865234375, 0.0, 0.0],
        [162.36328125, 0.0, 0.0], [162.861328125, 0.0, 0.0],
        [163.359375, 0.0, 0.0], [163.857421875, 0.0, 0.0],
        [164.35546875, 0.0, 0.0], [164.853515625, 0.0, 0.0],
        [165.3515625, 0.0, 0.0], [165.849609375, 0.0, 0.0],
        [166.34765625, 0.0, 0.0], [166.845703125, 0.0, 0.0],
        [167.34375, 0.0, 0.0], [167.841796875, 0.0, 0.0],
        [168.33984375, 0.0, 0.0], [168.837890625, 0.0, 0.0],
        [169.3359375, 0.0, 0.0], [169.833984375, 0.0, 0.0],
        [170.33203125, 0.0, 0.0], [170.830078125, 0.0, 0.0],
        [171.328125, 0.0, 0.0], [171.826171875, 0.0, 0.0],
        [172.32421875, 0.0, 0.0], [172.822265625, 0.0, 0.0],
        [173.3203125, 0.0, 0.0], [173.818359375, 0.0, 0.0],
        [174.31640625, 0.0, 0.0], [174.814453125, 0.0, 0.0],
        [175.3125, 0.0, 0.0], [175.810546875, 0.0, 0.0],
        [176.30859375, 0.0, 0.0], [176.806640625, 0.0, 0.0],
        [177.3046875, 0.0, 0.0], [177.802734375, 0.0, 0.0],
        [178.30078125, 0.0, 0.0], [178.798828125, 0.0, 0.0],
        [179.296875, 0.0, 0.0], [179.794921875, 0.0, 0.0],
        [180.29296875, 0.0, 0.0], [180.791015625, 0.0, 0.0],
        [181.2890625, 0.0, 0.0], [181.787109375, 0.0, 0.0],
        [182.28515625, 0.0, 0.0], [182.783203125, 0.0, 0.0],
        [183.28125, 0.0, 0.0], [183.779296875, 0.0, 0.0],
        [184.27734375, 0.0, 0.0], [184.775390625, 0.0, 0.0],
        [185.2734375, 0.0, 0.0], [185.771484375, 0.0, 0.0],
        [186.26953125, 0.0, 0.0], [186.767578125, 0.0, 0.0],
        [187.265625, 0.0, 0.0], [187.763671875, 0.0, 0.0],
        [188.26171875, 0.0, 0.0], [188.759765625, 0.0, 0.0],
        [189.2578125, 0.0, 0.0], [189.755859375, 0.0, 0.0],
        [190.25390625, 0.0, 0.0], [190.751953125, 0.0, 0.0],
        [191.25, 0.0, 0.0], [191.748046875, 0.0, 0.0],
        [192.24609375, 0.0, 0.0], [192.744140625, 0.0, 0.0],
        [193.2421875, 0.0, 0.0], [193.740234375, 0.0, 0.0],
        [194.23828125, 0.0, 0.0], [194.736328125, 0.0, 0.0],
        [195.234375, 0.0, 0.0], [195.732421875, 0.0, 0.0],
        [196.23046875, 0.0, 0.0], [196.728515625, 0.0, 0.0],
        [197.2265625, 0.0, 0.0], [197.724609375, 0.0, 0.0],
        [198.22265625, 0.0, 0.0], [198.720703125, 0.0, 0.0],
        [199.21875, 0.0, 0.0], [199.716796875, 0.0, 0.0],
        [200.21484375, 0.0, 0.0], [200.712890625, 0.0, 0.0],
        [201.2109375, 0.0, 0.0], [201.708984375, 0.0, 0.0],
        [202.20703125, 0.0, 0.0], [202.705078125, 0.0, 0.0],
        [203.203125, 0.0, 0.0], [203.701171875, 0.0, 0.0],
        [204.19921875, 0.0, 0.0], [204.697265625, 0.0, 0.0],
        [205.1953125, 0.0, 0.0], [205.693359375, 0.0, 0.0],
        [206.19140625, 0.0, 0.0], [206.689453125, 0.0, 0.0],
        [207.1875, 0.0, 0.0], [207.685546875, 0.0, 0.0],
        [208.18359375, 0.0, 0.0], [208.681640625, 0.0, 0.0],
        [209.1796875, 0.0, 0.0], [209.677734375, 0.0, 0.0],
        [210.17578125, 0.0, 0.0], [210.673828125, 0.0, 0.0],
        [211.171875, 0.0, 0.0], [211.669921875, 0.0, 0.0],
        [212.16796875, 0.0, 0.0], [212.666015625, 0.0, 0.0],
        [213.1640625, 0.0, 0.0], [213.662109375, 0.0, 0.0],
        [214.16015625, 0.0, 0.0], [214.658203125, 0.0, 0.0],
        [215.15625, 0.0, 0.0], [215.654296875, 0.0, 0.0],
        [216.15234375, 0.0, 0.0], [216.650390625, 0.0, 0.0],
        [217.1484375, 0.0, 0.0], [217.646484375, 0.0, 0.0],
        [218.14453125, 0.0, 0.0], [218.642578125, 0.0, 0.0],
        [219.140625, 0.0, 0.0], [219.638671875, 0.0, 0.0],
        [220.13671875, 0.0, 0.0], [220.634765625, 0.0, 0.0],
        [221.1328125, 0.0, 0.0], [221.630859375, 0.0, 0.0],
        [222.12890625, 0.0, 0.0], [222.626953125, 0.0, 0.0],
        [223.125, 0.0, 0.0], [223.623046875, 0.0, 0.0],
        [224.12109375, 0.0, 0.0], [224.619140625, 0.0, 0.0],
        [225.1171875, 0.0, 0.0], [225.615234375, 0.0, 0.0],
        [226.11328125, 0.0, 0.0], [226.611328125, 0.0, 0.0],
        [227.109375, 0.0, 0.0], [227.607421875, 0.0, 0.0],
        [228.10546875, 0.0, 0.0], [228.603515625, 0.0, 0.0],
        [229.1015625, 0.0, 0.0], [229.599609375, 0.0, 0.0],
        [230.09765625, 0.0, 0.0], [230.595703125, 0.0, 0.0],
        [231.09375, 0.0, 0.0], [231.591796875, 0.0, 0.0],
        [232.08984375, 0.0, 0.0], [232.587890625, 0.0, 0.0],
        [233.0859375, 0.0, 0.0], [233.583984375, 0.0, 0.0],
        [234.08203125, 0.0, 0.0], [234.580078125, 0.0, 0.0],
        [235.078125, 0.0, 0.0], [235.576171875, 0.0, 0.0],
        [236.07421875, 0.0, 0.0], [236.572265625, 0.0, 0.0],
        [237.0703125, 0.0, 0.0], [237.568359375, 0.0, 0.0],
        [238.06640625, 0.0, 0.0], [238.564453125, 0.0, 0.0],
        [239.0625, 0.0, 0.0], [239.560546875, 0.0, 0.0],
        [240.05859375, 0.0, 0.0], [240.556640625, 0.0, 0.0],
        [241.0546875, 0.0, 0.0], [241.552734375, 0.0, 0.0],
        [242.05078125, 0.0, 0.0], [242.548828125, 0.0, 0.0],
        [243.046875, 0.0, 0.0], [243.544921875, 0.0, 0.0],
        [244.04296875, 0.0, 0.0], [244.541015625, 0.0, 0.0],
        [245.0390625, 0.0, 0.0], [245.537109375, 0.0, 0.0],
        [246.03515625, 0.0, 0.0], [246.533203125, 0.0, 0.0],
        [247.03125, 0.0, 0.0], [247.529296875, 0.0, 0.0],
        [248.02734375, 0.0, 0.0], [248.525390625, 0.0, 0.0],
        [249.0234375, 0.0, 0.0], [249.521484375, 0.0, 0.0],
        [250.01953125, 0.0, 0.0], [250.517578125, 0.0, 0.0],
        [251.015625, 0.0, 0.0], [251.513671875, 0.0, 0.0],
        [252.01171875, 0.0, 0.0], [252.509765625, 0.0, 0.0],
        [253.0078125, 0.0, 0.0], [253.505859375, 0.0, 0.0],
        [254.00390625, 0.0, 0.0], [255.0, 0.0, 0.0]
    ],
    GREEN_COLORMAP: [
        [0.0, 0.0, 0.0], [0.0, 38.952755905, 0.0],
        [0.0, 77.90551181, 0.0], [0.0, 78.608267715, 0.0],
        [0.0, 79.31102362, 0.0], [0.0, 80.01377952499999, 0.0],
        [0.0, 80.71653543, 0.0], [0.0, 81.419291335, 0.0],
        [0.0, 82.12204724, 0.0], [0.0, 82.82480315000001, 0.0],
        [0.0, 83.52755906, 0.0], [0.0, 84.23031496499999, 0.0],
        [0.0, 84.93307087, 0.0], [0.0, 85.635826775, 0.0],
        [0.0, 86.33858268, 0.0], [0.0, 87.041338585, 0.0],
        [0.0, 87.74409449, 0.0], [0.0, 88.446850395, 0.0],
        [0.0, 89.1496063, 0.0], [0.0, 89.85236220499999, 0.0],
        [0.0, 90.55511811, 0.0], [0.0, 91.257874015, 0.0],
        [0.0, 91.96062992, 0.0], [0.0, 92.663385825, 0.0],
        [0.0, 93.36614173, 0.0], [0.0, 94.068897635, 0.0],
        [0.0, 94.77165354, 0.0], [0.0, 95.47440944499999, 0.0],
        [0.0, 96.17716535, 0.0], [0.0, 96.87992126, 0.0],
        [0.0, 97.58267717, 0.0], [0.0, 98.285433075, 0.0],
        [0.0, 98.98818898, 0.0], [0.0, 99.690944885, 0.0],
        [0.0, 100.39370079, 0.0], [0.0, 101.096456695, 0.0],
        [0.0, 101.7992126, 0.0], [0.0, 102.50196850500001, 0.0],
        [0.0, 103.20472441, 0.0], [0.0, 103.907480315, 0.0],
        [0.0, 104.61023622, 0.0], [0.0, 105.312992125, 0.0],
        [0.0, 106.01574803, 0.0], [0.0, 106.718503935, 0.0],
        [0.0, 107.42125984, 0.0], [0.0, 108.12401574500001, 0.0],
        [0.0, 108.82677165, 0.0], [0.0, 109.529527555, 0.0],
        [0.0, 110.23228346, 0.0], [0.0, 110.93503937, 0.0],
        [0.0, 111.63779528, 0.0], [0.0, 112.34055118500001, 0.0],
        [0.0, 113.04330709, 0.0], [0.0, 113.746062995, 0.0],
        [0.0, 114.4488189, 0.0], [0.0, 115.151574805, 0.0],
        [0.0, 115.85433071, 0.0], [0.0, 116.557086615, 0.0],
        [0.0, 117.25984252, 0.0], [0.0, 117.96259842500001, 0.0],
        [0.0, 118.66535433, 0.0], [0.0, 119.368110235, 0.0],
        [0.0, 120.07086614, 0.0], [0.0, 120.773622045, 0.0],
        [0.0, 121.47637795, 0.0], [0.0, 122.179133855, 0.0],
        [0.0, 122.88188976, 0.0], [0.0, 123.58464566500001, 0.0],
        [0.0, 124.28740157, 0.0], [0.0, 124.99015748, 0.0],
        [0.0, 125.69291339, 0.0], [0.0, 126.395669295, 0.0],
        [0.0, 127.0984252, 0.0], [0.0, 127.80118110499998, 0.0],
        [0.0, 128.50393701, 0.0], [0.0, 129.206692915, 0.0],
        [0.0, 129.90944882, 0.0], [0.0, 130.612204725, 0.0],
        [0.0, 131.31496063, 0.0], [0.0, 132.017716535, 0.0],
        [0.0, 132.72047244, 0.0], [0.0, 133.42322834499998, 0.0],
        [0.0, 134.12598425, 0.0], [0.0, 134.828740155, 0.0],
        [0.0, 135.53149606, 0.0], [0.0, 136.234251965, 0.0],
        [0.0, 136.93700787, 0.0], [0.0, 137.63976378, 0.0],
        [0.0, 138.34251969, 0.0], [0.0, 139.045275595, 0.0],
        [0.0, 139.7480315, 0.0], [0.0, 140.450787405, 0.0],
        [0.0, 141.15354331, 0.0], [0.0, 141.856299215, 0.0],
        [0.0, 142.55905512, 0.0], [0.0, 143.261811025, 0.0],
        [0.0, 143.96456693, 0.0], [0.0, 144.667322835, 0.0],
        [0.0, 145.37007874, 0.0], [0.0, 146.072834645, 0.0],
        [0.0, 146.77559055, 0.0], [0.0, 147.478346455, 0.0],
        [0.0, 148.18110236, 0.0], [0.0, 148.88385826500001, 0.0],
        [0.0, 149.58661417, 0.0], [0.0, 150.289370075, 0.0],
        [0.0, 150.99212598, 0.0], [0.0, 151.69488189, 0.0],
        [0.0, 152.3976378, 0.0], [0.0, 153.100393705, 0.0],
        [0.0, 153.80314961, 0.0], [0.0, 154.505905515, 0.0],
        [0.0, 155.20866142, 0.0], [0.0, 155.911417325, 0.0],
        [0.0, 156.61417323, 0.0], [0.0, 157.316929135, 0.0],
        [0.0, 158.01968504, 0.0], [0.0, 158.72244094500002, 0.0],
        [0.0, 159.42519685, 0.0], [0.0, 160.127952755, 0.0],
        [0.0, 160.83070866, 0.0], [0.0, 161.533464565, 0.0],
        [0.0, 162.23622047, 0.0], [0.0, 162.938976375, 0.0],
        [0.0, 163.64173228, 0.0], [0.0, 164.344488185, 0.0],
        [0.0, 165.04724409, 0.0], [0.0, 165.75, 0.0],
        [0.0, 166.45275591, 0.0], [0.0, 167.155511815, 0.0],
        [0.0, 167.85826772, 0.0], [0.0, 168.561023625, 0.0],
        [0.0, 169.26377953, 0.0], [0.0, 169.966535435, 0.0],
        [0.0, 170.66929134, 0.0], [0.0, 171.372047245, 0.0],
        [0.0, 172.07480315, 0.0], [0.0, 172.77755905499998, 0.0],
        [0.0, 173.48031496, 0.0], [0.0, 174.183070865, 0.0],
        [0.0, 174.88582677, 0.0], [0.0, 175.588582675, 0.0],
        [0.0, 176.29133858, 0.0], [0.0, 176.994094485, 0.0],
        [0.0, 177.69685039, 0.0], [0.0, 178.399606295, 0.0],
        [0.0, 179.1023622, 0.0], [0.0, 179.80511811, 0.0],
        [0.0, 180.50787402, 0.0], [0.0, 181.210629925, 0.0],
        [0.0, 181.91338583, 0.0], [0.0, 182.61614173499999, 0.0],
        [0.0, 183.31889764, 0.0], [0.0, 184.021653545, 0.0],
        [0.0, 184.72440945, 0.0], [0.0, 185.427165355, 0.0],
        [0.0, 186.12992126, 0.0], [0.0, 186.832677165, 0.0],
        [0.0, 187.53543307, 0.0], [0.0, 188.238188975, 0.0],
        [0.0, 188.94094488, 0.0], [0.0, 189.643700785, 0.0],
        [0.0, 190.34645669, 0.0], [0.0, 191.049212595, 0.0],
        [0.0, 191.7519685, 0.0], [0.0, 192.454724405, 0.0],
        [0.0, 193.15748031, 0.0], [0.0, 193.86023622, 0.0],
        [0.0, 194.56299213, 0.0], [0.0, 195.265748035, 0.0],
        [0.0, 195.96850394, 0.0], [0.0, 196.671259845, 0.0],
        [0.0, 197.37401575, 0.0], [0.0, 198.07677165500002, 0.0],
        [0.0, 198.77952756, 0.0], [0.0, 199.482283465, 0.0],
        [0.0, 200.18503937, 0.0], [0.0, 200.887795275, 0.0],
        [0.0, 201.59055118, 0.0], [0.0, 202.293307085, 0.0],
        [0.0, 202.99606299, 0.0], [0.0, 203.698818895, 0.0],
        [0.0, 204.4015748, 0.0], [0.0, 205.104330705, 0.0],
        [0.0, 205.80708661, 0.0], [0.0, 206.50984252, 0.0],
        [0.0, 207.21259843, 0.0], [0.0, 207.91535433500002, 0.0],
        [0.0, 208.61811024, 0.0], [0.0, 209.320866145, 0.0],
        [0.0, 210.02362205, 0.0], [0.0, 210.726377955, 0.0],
        [0.0, 211.42913386, 0.0], [0.0, 212.13188976499998, 0.0],
        [0.0, 212.83464567, 0.0], [0.0, 213.537401575, 0.0],
        [0.0, 214.24015748, 0.0], [0.0, 214.942913385, 0.0],
        [0.0, 215.64566929, 0.0], [0.0, 216.348425195, 0.0],
        [0.0, 217.0511811, 0.0], [0.0, 217.753937005, 0.0],
        [0.0, 218.45669291, 0.0], [0.0, 219.159448815, 0.0],
        [0.0, 219.86220472, 0.0], [0.0, 220.56496063, 0.0],
        [0.0, 221.26771654, 0.0], [0.0, 221.97047244499998, 0.0],
        [0.0, 222.67322835, 0.0], [0.0, 223.375984255, 0.0],
        [0.0, 224.07874016, 0.0], [0.0, 224.781496065, 0.0],
        [0.0, 225.48425197, 0.0], [0.0, 226.187007875, 0.0],
        [0.0, 226.88976378, 0.0], [0.0, 227.592519685, 0.0],
        [0.0, 228.29527559, 0.0], [0.0, 228.998031495, 0.0],
        [0.0, 229.7007874, 0.0], [0.0, 230.403543305, 0.0],
        [0.0, 231.10629921, 0.0], [0.0, 231.809055115, 0.0],
        [0.0, 232.51181102, 0.0], [0.0, 233.21456692499999, 0.0],
        [0.0, 233.91732283, 0.0], [0.0, 234.62007874, 0.0],
        [0.0, 235.32283465, 0.0], [0.0, 236.025590555, 0.0],
        [0.0, 236.72834646, 0.0], [0.0, 237.43110236500002, 0.0],
        [0.0, 238.13385827, 0.0], [0.0, 238.836614175, 0.0],
        [0.0, 239.53937008, 0.0], [0.0, 240.242125985, 0.0],
        [0.0, 240.94488189, 0.0], [0.0, 241.647637795, 0.0],
        [0.0, 242.3503937, 0.0], [0.0, 243.053149605, 0.0],
        [0.0, 243.75590551, 0.0], [0.0, 244.458661415, 0.0],
        [0.0, 245.16141732, 0.0], [0.0, 245.864173225, 0.0],
        [0.0, 246.56692913, 0.0], [0.0, 247.269685035, 0.0],
        [0.0, 247.97244094, 0.0], [0.0, 248.67519685000002, 0.0],
        [0.0, 249.37795276, 0.0], [0.0, 250.080708665, 0.0],
        [0.0, 250.78346457, 0.0], [0.0, 251.486220475, 0.0],
        [0.0, 252.18897638, 0.0], [0.0, 252.891732285, 0.0],
        [0.0, 253.59448819, 0.0], [0.0, 254.297244095, 0.0],
        [0.0, 255.0, 0.0], [0.0, 255.0, 0.0]
    ],
    VIRIDIS_COLORMAP: [
        [68, 1, 84], [68, 2, 85], [68, 3, 87], [69, 5, 88],
        [69, 6, 90], [69, 8, 91], [70, 9, 92], [70, 11, 94],
        [70, 12, 95], [70, 14, 97], [71, 15, 98], [71, 17, 99],
        [71, 18, 101], [71, 20, 102], [71, 21, 103], [71, 22, 105],
        [71, 24, 106], [72, 25, 107], [72, 26, 108], [72, 28, 110],
        [72, 29, 111], [72, 30, 112], [72, 32, 113], [72, 33, 114],
        [72, 34, 115], [72, 35, 116], [71, 37, 117], [71, 38, 118],
        [71, 39, 119], [71, 40, 120], [71, 42, 121], [71, 43, 122],
        [71, 44, 123], [70, 45, 124], [70, 47, 124], [70, 48, 125],
        [70, 49, 126], [69, 50, 127], [69, 52, 127], [69, 53, 128],
        [69, 54, 129], [68, 55, 129], [68, 57, 130], [67, 58, 131],
        [67, 59, 131], [67, 60, 132], [66, 61, 132], [66, 62, 133],
        [66, 64, 133], [65, 65, 134], [65, 66, 134], [64, 67, 135],
        [64, 68, 135], [63, 69, 135], [63, 71, 136], [62, 72, 136],
        [62, 73, 137], [61, 74, 137], [61, 75, 137], [61, 76, 137],
        [60, 77, 138], [60, 78, 138], [59, 80, 138], [59, 81, 138],
        [58, 82, 139], [58, 83, 139], [57, 84, 139], [57, 85, 139],
        [56, 86, 139], [56, 87, 140], [55, 88, 140], [55, 89, 140],
        [54, 90, 140], [54, 91, 140], [53, 92, 140], [53, 93, 140],
        [52, 94, 141], [52, 95, 141], [51, 96, 141], [51, 97, 141],
        [50, 98, 141], [50, 99, 141], [49, 100, 141], [49, 101, 141],
        [49, 102, 141], [48, 103, 141], [48, 104, 141], [47, 105, 141],
        [47, 106, 141], [46, 107, 142], [46, 108, 142], [46, 109, 142],
        [45, 110, 142], [45, 111, 142], [44, 112, 142], [44, 113, 142],
        [44, 114, 142], [43, 115, 142], [43, 116, 142], [42, 117, 142],
        [42, 118, 142], [42, 119, 142], [41, 120, 142], [41, 121, 142],
        [40, 122, 142], [40, 122, 142], [40, 123, 142], [39, 124, 142],
        [39, 125, 142], [39, 126, 142], [38, 127, 142], [38, 128, 142],
        [38, 129, 142], [37, 130, 142], [37, 131, 141], [36, 132, 141],
        [36, 133, 141], [36, 134, 141], [35, 135, 141], [35, 136, 141],
        [35, 137, 141], [34, 137, 141], [34, 138, 141], [34, 139, 141],
        [33, 140, 141], [33, 141, 140], [33, 142, 140], [32, 143, 140],
        [32, 144, 140], [32, 145, 140], [31, 146, 140], [31, 147, 139],
        [31, 148, 139], [31, 149, 139], [31, 150, 139], [30, 151, 138],
        [30, 152, 138], [30, 153, 138], [30, 153, 138], [30, 154, 137],
        [30, 155, 137], [30, 156, 137], [30, 157, 136], [30, 158, 136],
        [30, 159, 136], [30, 160, 135], [31, 161, 135], [31, 162, 134],
        [31, 163, 134], [32, 164, 133], [32, 165, 133], [33, 166, 133],
        [33, 167, 132], [34, 167, 132], [35, 168, 131], [35, 169, 130],
        [36, 170, 130], [37, 171, 129], [38, 172, 129], [39, 173, 128],
        [40, 174, 127], [41, 175, 127], [42, 176, 126], [43, 177, 125],
        [44, 177, 125], [46, 178, 124], [47, 179, 123], [48, 180, 122],
        [50, 181, 122], [51, 182, 121], [53, 183, 120], [54, 184, 119],
        [56, 185, 118], [57, 185, 118], [59, 186, 117], [61, 187, 116],
        [62, 188, 115], [64, 189, 114], [66, 190, 113], [68, 190, 112],
        [69, 191, 111], [71, 192, 110], [73, 193, 109], [75, 194, 108],
        [77, 194, 107], [79, 195, 105], [81, 196, 104], [83, 197, 103],
        [85, 198, 102], [87, 198, 101], [89, 199, 100], [91, 200, 98],
        [94, 201, 97], [96, 201, 96], [98, 202, 95], [100, 203, 93],
        [103, 204, 92], [105, 204, 91], [107, 205, 89], [109, 206, 88],
        [112, 206, 86], [114, 207, 85], [116, 208, 84], [119, 208, 82],
        [121, 209, 81], [124, 210, 79], [126, 210, 78], [129, 211, 76],
        [131, 211, 75], [134, 212, 73], [136, 213, 71], [139, 213, 70],
        [141, 214, 68], [144, 214, 67], [146, 215, 65], [149, 215, 63],
        [151, 216, 62], [154, 216, 60], [157, 217, 58], [159, 217, 56],
        [162, 218, 55], [165, 218, 53], [167, 219, 51], [170, 219, 50],
        [173, 220, 48], [175, 220, 46], [178, 221, 44], [181, 221, 43],
        [183, 221, 41], [186, 222, 39], [189, 222, 38], [191, 223, 36],
        [194, 223, 34], [197, 223, 33], [199, 224, 31], [202, 224, 30],
        [205, 224, 29], [207, 225, 28], [210, 225, 27], [212, 225, 26],
        [215, 226, 25], [218, 226, 24], [220, 226, 24], [223, 227, 24],
        [225, 227, 24], [228, 227, 24], [231, 228, 25], [233, 228, 25],
        [236, 228, 26], [238, 229, 27], [241, 229, 28], [243, 229, 30],
        [246, 230, 31], [248, 230, 33], [250, 230, 34], [253, 231, 36]
    ],
    PINK_COLORMAP: [],
    // Corresponds to the PiYG palette.
    PINK_WHITE_GREEN_COLORMAP: Object(_utils__WEBPACK_IMPORTED_MODULE_1__["range"])(128).map(function (i) { return [255, i * 2, 255]; }),
    COLOR_MAPS: {}
};
colors.PINK_COLORMAP = Object(_utils__WEBPACK_IMPORTED_MODULE_1__["range"])(256).map(function (i) { return [colors.RED_COLORMAP[i][0], 0, colors.RED_COLORMAP[i][0]]; });
var pinkWhiteColors = Object(_utils__WEBPACK_IMPORTED_MODULE_1__["range"])(128).map(function (i) { return [255 - 2 * i, 255, 255 - 2 * i]; });
(_a = colors.PINK_WHITE_GREEN_COLORMAP).push.apply(_a, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(pinkWhiteColors));
colors.COLOR_MAPS = {
    'red_green': { 'positive': colors.GREEN_COLORMAP, 'negative': colors.RED_COLORMAP },
    'red': { 'positive': colors.RED_COLORMAP, 'negative': colors.RED_COLORMAP },
    'green': { 'positive': colors.GREEN_COLORMAP, 'negative': colors.GREEN_COLORMAP },
    'viridis': {
        'positive': colors.VIRIDIS_COLORMAP,
        'negative': colors.VIRIDIS_COLORMAP
    },
    'pink_white_green': {
        'positive': colors.PINK_WHITE_GREEN_COLORMAP,
        'negative': colors.PINK_WHITE_GREEN_COLORMAP
    },
    'pink_green': { 'positive': colors.GREEN_COLORMAP, 'negative': colors.PINK_COLORMAP }
};
// LINT.ThenChange(//depot/google3/cloud/ml/explainability/explainers/common/constants.py)


/***/ }),

/***/ "./src/img_feature_attr/feature_attr_service.ts":
/*!******************************************************!*\
  !*** ./src/img_feature_attr/feature_attr_service.ts ***!
  \******************************************************/
/*! exports provided: FeatureAttrService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FeatureAttrService", function() { return FeatureAttrService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _image_explanation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image_explanation */ "./src/img_feature_attr/image_explanation.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/http.js");







/**
 * A service for loading and holding explanation data.
 * LoadDataEvents will be triggered from the widget.
 */
var FeatureAttrService = /** @class */ (function () {
    function FeatureAttrService(http) {
        var _this = this;
        this.http = http;
        this.imgExplanation = new _image_explanation__WEBPACK_IMPORTED_MODULE_4__["ImageExplanation"]();
        this.imgExplanationSource = new rxjs__WEBPACK_IMPORTED_MODULE_2__["ReplaySubject"](1);
        this.imgAttrVectorSource = new rxjs__WEBPACK_IMPORTED_MODULE_2__["ReplaySubject"](1);
        this.errorMessages = [];
        // Handle on-destroy Subject, used to unsubscribe.
        this.destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_2__["ReplaySubject"](1);
        // Bind this to ensure correct caller
        this.updateAttrRange = this.updateAttrRange.bind(this);
        // Set to react to the load data event (from dict object)
        Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["fromEvent"])(document, 'loadDataFromDictEvent')
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(this.destroyed))
            .subscribe(function (e) {
            var dataEvent = e;
            _this.loadDataFromDict(dataEvent.detail.data, dataEvent.detail.metadata);
        });
        // Set to react to the load data event (from json string)
        Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["fromEvent"])(document, 'loadDataFromJsonEvent')
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(this.destroyed))
            .subscribe(function (e) {
            var dataEvent = e;
            var metadata = JSON.parse(dataEvent.detail.metadata);
            var data = JSON.parse(dataEvent.detail.data);
            _this.loadDataFromDict(data, metadata);
        });
        // Set to react to the load data event (from an url)
        Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["fromEvent"])(document, 'loadDataFromUrlEvent')
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(this.destroyed))
            .subscribe(function (e) {
            var dataEvent = e;
            _this.loadDataFromUrl(dataEvent.detail.dataUrl, dataEvent.detail.metadataUrl);
        });
    }
    /**
     * Given a json object and the input tensor, initialize
     * the imgExplanation, and notify the subscribers to update.
     */
    FeatureAttrService.prototype.loadDataFromDict = function (data, metadata) {
        this.imgExplanation.initialize(data, metadata);
        this.imgExplanationSource.next(this.imgExplanation);
        this.imgAttrVectorSource.next(this.imgExplanation.toVector());
    };
    /**
     * Given an url and the input tensor, fetch the json file and trigger
     * loadDataFromJson. If fails, show error messages.
     */
    FeatureAttrService.prototype.loadDataFromUrl = function (dataUrl, metadataUrl) {
        var _this = this;
        var data = this.http.get(dataUrl);
        var metadata = this.http.get(metadataUrl);
        Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["zip"])(data, metadata).subscribe({
            next: function (_a) {
                var _b = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__read"])(_a, 2), dataResponse = _b[0], metadataResponse = _b[1];
                _this.loadDataFromDict(dataResponse, metadataResponse);
            },
            error: function (err) {
                _this.errorMessages.push(err.error);
            }
        });
    };
    /**
     * Set current explanation's visible
     * attribution range. This update will triger the ImgFeatureAttr component to
     * update.
     */
    FeatureAttrService.prototype.updateAttrRange = function (minVal, maxVal) {
        this.imgExplanation.setVisibleRange(minVal, maxVal);
        this.imgExplanationSource.next(this.imgExplanation);
    };
    /** Update post processor for new visualization configs */
    FeatureAttrService.prototype.updatePostProcessor = function (visualizationConfig) {
        this.imgExplanation.updatePostProcessor(visualizationConfig);
        this.imgExplanationSource.next(this.imgExplanation);
    };
    /**
     * Get the image explanation object.
     */
    FeatureAttrService.prototype.getImageExplanation = function () {
        return this.imgExplanation;
    };
    /**
     * Unsubscribe all pending subscriptions via this.destroyed
     */
    FeatureAttrService.prototype.ngOnDestroy = function () {
        this.destroyed.next();
        this.destroyed.complete();
    };
    FeatureAttrService.ɵfac = function FeatureAttrService_Factory(t) { return new (t || FeatureAttrService)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵinject"](_angular_common_http__WEBPACK_IMPORTED_MODULE_5__["HttpClient"])); };
    FeatureAttrService.ɵprov = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineInjectable"]({ token: FeatureAttrService, factory: FeatureAttrService.ɵfac, providedIn: 'root' });
    return FeatureAttrService;
}());

/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵsetClassMetadata"](FeatureAttrService, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"],
        args: [{ providedIn: 'root' }]
    }], function () { return [{ type: _angular_common_http__WEBPACK_IMPORTED_MODULE_5__["HttpClient"] }]; }, null); })();


/***/ }),

/***/ "./src/img_feature_attr/image_explanation.ts":
/*!***************************************************!*\
  !*** ./src/img_feature_attr/image_explanation.ts ***!
  \***************************************************/
/*! exports provided: ImageExplanation */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageExplanation", function() { return ImageExplanation; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _outline_post_processor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./outline_post_processor */ "./src/img_feature_attr/outline_post_processor.ts");
/* harmony import */ var _pixel_post_processor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pixel_post_processor */ "./src/img_feature_attr/pixel_post_processor.ts");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/**
 * @fileoverview This file contains the definition of the Explanation class.
 * The explanation instance can be initialized with explanation data in json
 * format.
 */





/** Typeguard for VisualizationConfig */
function isVisualizationConfig(config) {
    return config.hasOwnProperty('type');
}
/**
 * ImageExplanation class contains information about the images, including
 * attributions the original image, and other explanation related properties for
 * visualization.
 */
var ImageExplanation = /** @class */ (function () {
    function ImageExplanation() {
        this.attrs = [];
        this.attrs2D = [];
        this.attrs3D = [];
        this.image = [];
        this.image2D = [];
        this.image3D = [];
        this.posPostProcessedImage = [];
        this.negPostProcessedImage = [];
        this.inputName = '';
        this.imageWidth = 0;
        this.imageHeight = 0;
        this.maxAttrVal = 0;
        this.imageData = new ImageData(1, 1); // placeholder image data
        this.posPostProcessedImageData =
            new ImageData(1, 1); // placeholder image data
        this.negPostProcessedImageData =
            new ImageData(1, 1); // placeholder image data
        this.isFiltered = false;
        this.minVisibleVal = -1;
        this.maxVisibleVal = -1;
        this.hasInitialized = false;
        this.postProcessorType = 'pixels';
        this.posPostProcessor =
            _pixel_post_processor__WEBPACK_IMPORTED_MODULE_3__["PixelPostProcessor"].fromDict({ 'type': 'pixels', 'polarity': 'positive' });
        this.negPostProcessor =
            _pixel_post_processor__WEBPACK_IMPORTED_MODULE_3__["PixelPostProcessor"].fromDict({ 'type': 'pixels', 'polarity': 'negative' });
        this.metadata = undefined;
        this.visualizationConfig = { 'type': 'pixels' };
        this.domain = {};
    }
    /**
     * Initialize the explanation from attribution json for a RGB
     * image. The attributions will come in as three dimension (the innest one is
     * attributions to R, G, B channels). We will sum up the three-channel
     * attributions to make the attributions simply pixel-based.
     */
    ImageExplanation.prototype.initialize = function (data, metadata) {
        var _a, _b;
        this.inputName = Object.keys(metadata.inputs)[0];
        this.attrs = data['debug_raw_attribution_dict'][this.inputName];
        this.image = data['debug_input_values'][this.inputName];
        this.metadata = metadata;
        var inputMetadata = metadata.inputs[this.inputName];
        var visualizationConfig = (_a = inputMetadata.visualization, (_a !== null && _a !== void 0 ? _a : {}));
        var domain = (_b = inputMetadata.domain, (_b !== null && _b !== void 0 ? _b : {}));
        this.domain = domain;
        if (isVisualizationConfig(visualizationConfig)) {
            this.updatePostProcessor(visualizationConfig);
        }
        // Ensure attrs and image has consistent dimensions
        this.specifyAttrsDimension();
        this.specifyImageDimension();
        // check image size
        this.deriveAndCheckImageSize();
        this.update();
    };
    ImageExplanation.prototype.updatePostProcessor = function (visualizationConfig) {
        if (visualizationConfig.type.toLowerCase() === 'pixels') {
            this.postProcessorType = 'pixels';
            var posConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__assign"])({}, visualizationConfig);
            posConfig.polarity = 'positive';
            this.posPostProcessor =
                _pixel_post_processor__WEBPACK_IMPORTED_MODULE_3__["PixelPostProcessor"].fromDict(posConfig, this.domain);
            var negConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__assign"])({}, visualizationConfig);
            negConfig.polarity = 'negative';
            this.negPostProcessor =
                _pixel_post_processor__WEBPACK_IMPORTED_MODULE_3__["PixelPostProcessor"].fromDict(negConfig, this.domain);
        }
        else if (visualizationConfig.type.toLowerCase() === 'outlines') {
            this.postProcessorType = 'outlines';
            var posConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__assign"])({}, visualizationConfig);
            posConfig.polarity = 'positive';
            this.posPostProcessor =
                _outline_post_processor__WEBPACK_IMPORTED_MODULE_2__["OutlinePostProcessor"].fromDict(posConfig, this.domain);
            var negConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__assign"])({}, visualizationConfig);
            negConfig.polarity = 'negative';
            this.negPostProcessor =
                _outline_post_processor__WEBPACK_IMPORTED_MODULE_2__["OutlinePostProcessor"].fromDict(negConfig, this.domain);
        }
        this.visualizationConfig = visualizationConfig;
    };
    /**
     * Convert the attributions to 1D array. This is used to plot the
     * histogram.
     */
    ImageExplanation.prototype.toVector = function () {
        return this.attrs2D.reduce(function (currentVector, newRow) { return Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(currentVector, newRow); });
    };
    /**
     * Set visible attribution range and the
     * filtering flag.
     */
    ImageExplanation.prototype.setVisibleRange = function (minVal, maxVal) {
        this.isFiltered = true;
        this.minVisibleVal = minVal;
        this.maxVisibleVal = maxVal;
    };
    /**
     * Reset the visible range to [-1, 1] and reset the
     * isFiltered flag to false.
     */
    ImageExplanation.prototype.resetVisibleRange = function () {
        this.isFiltered = false;
        this.minVisibleVal = -1;
        this.maxVisibleVal = 1;
    };
    /**
     * If the range is filtered, return attributions that fit
     * the filtering criteria. If not, return the raw attributions.
     */
    ImageExplanation.prototype.getVisibleAttrs = function () {
        var _this = this;
        if (this.isFiltered) {
            return this.attrs2D.map(function (row) { return row.map(function (val) {
                return (_this.minVisibleVal <= val && val <= _this.maxVisibleVal) ? val :
                    0;
            }); });
        }
        else {
            return this.attrs2D;
        }
    };
    /**
     * Initialize image data.
     */
    ImageExplanation.prototype.initializeImageData = function (scale, alpha) {
        if (scale === void 0) { scale = 1; }
        if (alpha === void 0) { alpha = 1.0; }
        this.imageData = this.createImageData(this.image3D, scale, alpha);
        this.updatePostProprocessedImageData(scale, alpha);
    };
    /**
     * Update post processed image data.
     */
    ImageExplanation.prototype.updatePostProprocessedImageData = function (scale, alpha) {
        if (scale === void 0) { scale = 1; }
        if (alpha === void 0) { alpha = 1.0; }
        var visibleAttrs = this.getVisibleAttrs();
        this.posPostProcessedImage = this.posPostProcessor ?
            this.posPostProcessor.process(visibleAttrs, this.image3D) :
            this.posPostProcessedImage;
        this.negPostProcessedImage = this.negPostProcessor ?
            this.negPostProcessor.process(visibleAttrs, this.image3D) :
            this.negPostProcessedImage;
        this.posPostProcessedImageData =
            this.createImageData(this.posPostProcessedImage, scale, alpha, 1);
        this.negPostProcessedImageData =
            this.createImageData(this.negPostProcessedImage, scale, alpha, 1);
    };
    /**
     * Based on the image matrix, create ImageData
     * object for plotting onto HTML Canvas. The ImageData does not support
     * scaling, and thus we implement scaling here when creating ImageData.
     */
    ImageExplanation.prototype.createImageData = function (imageMatrix, scale, alpha, base) {
        if (scale === void 0) { scale = 1.0; }
        if (alpha === void 0) { alpha = 1.0; }
        if (base === void 0) { base = 255; }
        var imageHeight = this.imageHeight;
        var imageWidth = this.imageWidth;
        var imageData = new ImageData(Math.round(imageWidth * scale), Math.round(imageHeight * scale));
        for (var rIdx = 0; rIdx < imageHeight; rIdx++) {
            for (var cIdx = 0; cIdx < imageWidth; cIdx++) {
                var arrIdx = (rIdx * imageWidth * scale + cIdx * scale) * 4;
                this.setScaledImageDataForOnePixel(imageMatrix, imageData, rIdx, cIdx, arrIdx, scale, alpha, base);
            }
        }
        return imageData;
    };
    /**
     * update(): Initialize image size, max attribution val, initialize image,
     * and reset visible range
     */
    ImageExplanation.prototype.update = function () {
        this.maxAttrVal = Object(_utils__WEBPACK_IMPORTED_MODULE_4__["findMaxVal"])(this.attrs2D);
        this.initializeImageData();
        this.resetVisibleRange();
        this.hasInitialized = true;
    };
    ImageExplanation.prototype.specifyAttrsDimension = function () {
        if (Object(_utils__WEBPACK_IMPORTED_MODULE_4__["isArray2D"])(this.attrs)) {
            // attrs is grey scale
            this.attrs2D = this.attrs;
            this.attrs3D = Object(_utils__WEBPACK_IMPORTED_MODULE_4__["unflatten2Dto3D"])(this.attrs2D, [1, 1, 1]);
        }
        else {
            // attrs is RGB
            this.attrs3D = this.attrs;
            this.attrs2D = Object(_utils__WEBPACK_IMPORTED_MODULE_4__["flatten3Dto2D"])(this.attrs3D, true);
        }
    };
    ImageExplanation.prototype.specifyImageDimension = function () {
        if (Object(_utils__WEBPACK_IMPORTED_MODULE_4__["isArray2D"])(this.image)) {
            // image is grey scale
            this.image2D = this.image;
            this.image3D = Object(_utils__WEBPACK_IMPORTED_MODULE_4__["unflatten2Dto3D"])(this.image2D, [1, 1, 1]);
        }
        else {
            // image is RGB
            this.image3D = this.image;
            this.image2D = Object(_utils__WEBPACK_IMPORTED_MODULE_4__["flatten3Dto2D"])(this.image3D);
        }
    };
    /**
     * Based on the image matrix, referring the size of the
     * image.
     */
    ImageExplanation.prototype.deriveAndCheckImageSize = function () {
        var imageMatrix = this.image3D;
        var attrMatrix = this.attrs3D;
        var imageHeight = imageMatrix.length;
        var imageWidth = imageHeight > 0 ? imageMatrix[0].length : 0;
        var attrHeight = attrMatrix.length;
        var attrWidth = attrHeight > 0 ? attrMatrix[0].length : 0;
        // check if the image is not visible or if attr size is different
        // from image size
        if (imageWidth === 0 || imageHeight === 0) {
            Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["throwError"])('Incorrect image size');
            return;
        }
        else if (imageWidth !== attrWidth || imageHeight !== attrHeight) {
            Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["throwError"])('Inconsistent image size and attribution size');
            return;
        }
        this.imageWidth = imageWidth;
        this.imageHeight = imageHeight;
    };
    /**
     *  A helper function for setting scaled image data for one pixel
     */
    ImageExplanation.prototype.setScaledImageDataForOnePixel = function (imageMatrix, imageData, rIdx, cIdx, arrIdx, scale, alpha, base) {
        if (base === void 0) { base = 255; }
        var imageWidth = this.imageWidth;
        for (var scaleRIdx = 0; scaleRIdx < scale; scaleRIdx++) {
            for (var scaleCIdx = 0; scaleCIdx < scale; scaleCIdx++) {
                var offset = arrIdx + 4 * (imageWidth * scaleRIdx + scaleCIdx);
                imageData.data[offset] = imageMatrix[rIdx][cIdx][0] * base;
                imageData.data[offset + 1] = imageMatrix[rIdx][cIdx][1] * base;
                imageData.data[offset + 2] = imageMatrix[rIdx][cIdx][2] * base;
                imageData.data[offset + 3] = alpha * 255;
            }
        }
    };
    return ImageExplanation;
}());



/***/ }),

/***/ "./src/img_feature_attr/image_processing.ts":
/*!**************************************************!*\
  !*** ./src/img_feature_attr/image_processing.ts ***!
  \**************************************************/
/*! exports provided: binaryErosion, binaryDilation, binaryHoleFilling, labelConnectedComponents */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "binaryErosion", function() { return binaryErosion; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "binaryDilation", function() { return binaryDilation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "binaryHoleFilling", function() { return binaryHoleFilling; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "labelConnectedComponents", function() { return labelConnectedComponents; });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/**
 * @fileoverview Typescript implementation of a set of image processing,
 * functions (i.e., morphological filtering, such as binary erosion and
 * binary dilation).
 */

function inBoundary(array2D, rIdx, cIdx) {
    return (0 <= rIdx && rIdx < array2D.length) &&
        (0 <= cIdx && cIdx < array2D[0].length);
}
var STRUCTURE_ELEMENT_DENSE = [[0, 0], [-1, 0], [0, 1], [1, 0], [0, -1]];
var BFS_DIRECTIONS = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]];
/**
 * Binary Erosion function.
 * Morphological filtering based on a structure element (which is fixed in this
 * implementation) to shrink the shape in a given 2D array.
 *
 * Moving the structure element over all the cells in the given 2D array.
 * If any of the cells covered by the structure element is not 1, then the
 * center of the structure element should be turned into 0 as well.
 *
 * The results will be saved into the output 2D array passed in the parameter,
 * and the return value indicates whether any element is modified in this
 * iteration.
 *
 * ==Example==
 *
 * A given 2D array:
 * [[0, 0, 0, 0, 0],
 *  [0, 1, 0, 1, 0],
 *  [0, 0, 0, 0, 0],
 *  [0, 0, 0, 1, 0],
 *  [0, 0, 1, 0, 0]]
 *
 * Structure element:
 * [[0, 1, 0],
 *  [1, 1, 1],
 *  [0, 1, 0]]
 *
 * Will become:
 * [[0, 1, 0, 1, 0],
 *  [1, 1, 1, 1, 1],
 *  [0, 1, 0, 1, 0],
 *  [0, 0, 1, 1, 1],
 *  [0, 1, 1, 1, 0]]
 */
function binaryErosion(array2D, invert) {
    if (invert === void 0) { invert = false; }
    if (array2D.length === 0 || array2D[0].length === 0) {
        throw new Error('The shape of the array cannot be zero.');
    }
    var canKeep = true;
    var results = [];
    for (var rIdx = 0; rIdx < array2D.length; rIdx++) {
        var newRow = [];
        for (var cIdx = 0; cIdx < array2D[rIdx].length; cIdx++) {
            canKeep = array2D[rIdx][cIdx] !== 0;
            for (var idx = 0; idx < STRUCTURE_ELEMENT_DENSE.length; idx++) {
                var ri = rIdx + STRUCTURE_ELEMENT_DENSE[idx][0];
                var ci = cIdx + STRUCTURE_ELEMENT_DENSE[idx][1];
                if (inBoundary(array2D, ri, ci)) {
                    if (array2D[ri][ci] === 0) {
                        canKeep = false;
                        break;
                    }
                }
                else if (!invert) {
                    canKeep = false;
                    break;
                }
            }
            newRow.push(canKeep ? 1 : 0);
        }
        results.push(newRow);
    }
    return results;
}
/**
 * Binary Dilation function.
 *
 * Morphological filtering based on a structure element (which is fixed in this
 * implementation) to expand the shape in a given 2D array.
 *
 * Moving the structure element over all the cells in the given 2D array.
 * If any of the cells covered by the structure element is 1, then the
 * center of the structure element should be turned into 1 as well.
 *
 * The results will be saved into the output 2D array passed in the parameter,
 * and the return value indicates whether any element is modified in this
 * iteration.
 *
 * ==Example==
 *
 * A given 2D array:
 * [[0, 0, 0, 0, 0],
 *  [0, 1, 0, 1, 0],
 *  [0, 0, 0, 0, 0],
 *  [0, 0, 0, 1, 0],
 *  [0, 0, 1, 0, 0]]
 *
 * Not:
 * [[1, 1, 1, 1, 1],
 *  [1, *, 1, *, 1],
 *  [1, 1, 1, 1, 1],
 *  [1, 1, 1, *, 1],
 *  [1, 1, *, 1, 1]]
 *
 * Erosion:
 * [[1, 0, 1, 0, 1],
 *  [0, *, 0, *, 0],
 *  [1, 0, 1, 0, 1],
 *  [1, 1, 0, *, 0],
 *  [1, 0, *, 0, 1]]
 *
 * Structure element:
 * [[0, 1, 0],
 *  [1, 1, 1],
 *  [0, 1, 0]]
 *
 * Will become:
 * [[0, 1, 0, 1, 0],
 *  [1, 1, 1, 1, 1],
 *  [0, 1, 0, 1, 0],
 *  [0, 0, 1, 1, 1],
 *  [0, 1, 1, 1, 0]]
 */
function binaryDilation(array2D, mask) {
    if (mask === void 0) { mask = null; }
    if (array2D.length === 0 || array2D[0].length === 0) {
        throw new Error('The shape of the array cannot be zero.');
    }
    var array2DComp = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["logicNotArray2D"])(array2D);
    var results = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["logicNotArray2D"])(binaryErosion(array2DComp, true));
    if (mask !== null) {
        if (mask.length !== results.length || results.length === 0 ||
            mask[0].length !== results[0].length) {
            throw new Error('Mask and inputs do not have the same shape.');
        }
        for (var rIdx = 0; rIdx < results.length; rIdx++) {
            for (var cIdx = 0; cIdx < results[rIdx].length; cIdx++) {
                // sets to zero if the corresponding mask cell is zero
                if (results[rIdx][cIdx] !== 0 && mask[rIdx][cIdx] === 0) {
                    results[rIdx][cIdx] = 0;
                }
            }
        }
    }
    return results;
}
function getBoundary(array2D) {
    if (array2D.length === 0 || array2D[0].length === 0) {
        throw new Error('The shape of the array cannot be zero.');
    }
    var results = array2D.map(function (row) { return row.map(function (val) { return 0; }); });
    var height = array2D.length;
    var width = array2D[0].length;
    for (var rIdx = 0; rIdx < height; rIdx++) {
        if (array2D[rIdx][0] !== 0) {
            results[rIdx][0] = 1;
        }
        if (array2D[rIdx][width - 1] !== 0) {
            results[rIdx][width - 1] = 1;
        }
    }
    for (var cIdx = 0; cIdx < width; cIdx++) {
        if (array2D[0][cIdx] !== 0) {
            results[0][cIdx] = 1;
        }
        if (array2D[height - 1][cIdx] !== 0) {
            results[height - 1][cIdx] = 1;
        }
    }
    return results;
}
/**
 * Binary hole filling
 */
function binaryHoleFilling(array2D) {
    if (array2D.length === 0 || array2D[0].length === 0) {
        throw new Error('The shape of the array cannot be zero.');
    }
    var array2DComp = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["logicNotArray2D"])(array2D);
    var marker = getBoundary(array2DComp);
    var inputs = marker;
    var hasNewlyFilledHoles = true;
    var height = inputs.length;
    var width = inputs[0].length;
    while (hasNewlyFilledHoles) {
        hasNewlyFilledHoles = false;
        var outputs = binaryDilation(inputs, array2DComp);
        for (var rIdx = 0; rIdx < height && !hasNewlyFilledHoles; rIdx++) {
            for (var cIdx = 0; cIdx < width && !hasNewlyFilledHoles; cIdx++) {
                if (inputs[rIdx][cIdx] !== outputs[rIdx][cIdx]) {
                    hasNewlyFilledHoles = true;
                }
            }
        }
        inputs = outputs;
    }
    return Object(_utils__WEBPACK_IMPORTED_MODULE_0__["logicNotArray2D"])(inputs);
}
function connectedComponentBFS(array2D, labels, srcR, srcC, label, indices) {
    if (indices === void 0) { indices = null; }
    var queue = [];
    queue.push([srcR, srcC]);
    while (queue.length > 0) {
        var head = queue[0];
        queue.shift();
        if (indices !== null) {
            indices.push(head);
        }
        for (var idx = 0; idx < BFS_DIRECTIONS.length; idx++) {
            var ri = head[0] + BFS_DIRECTIONS[idx][0];
            var ci = head[1] + BFS_DIRECTIONS[idx][1];
            if (inBoundary(array2D, ri, ci) && labels[ri][ci] === 0 &&
                array2D[ri][ci] === 1) {
                labels[ri][ci] = label;
                queue.push([ri, ci]);
            }
        }
    }
}
/**
 * Returns a 2D array connected component labels based on the given array.
 * If indicesList is given, also saves indices for each components into the
 * given list.
 */
function labelConnectedComponents(array2D, indicesList) {
    if (indicesList === void 0) { indicesList = null; }
    if (array2D.length === 0 || array2D[0].length === 0) {
        throw new Error('The shape of the array cannot be zero.');
    }
    var labels = array2D.map(function (row) { return row.map(function (v) { return 0; }); });
    var connectedComponentIdx = 0;
    for (var rIdx = 0; rIdx < array2D.length; rIdx++) {
        for (var cIdx = 0; cIdx < array2D[rIdx].length; cIdx++) {
            if (labels[rIdx][cIdx] === 0 && array2D[rIdx][cIdx] === 1) {
                connectedComponentIdx++;
                labels[rIdx][cIdx] = connectedComponentIdx;
                if (indicesList !== null) {
                    var indices = new Array();
                    connectedComponentBFS(array2D, labels, rIdx, cIdx, connectedComponentIdx, indices);
                    indicesList.push(indices);
                }
                else {
                    connectedComponentBFS(array2D, labels, rIdx, cIdx, connectedComponentIdx);
                }
            }
        }
    }
    return labels;
}


/***/ }),

/***/ "./src/img_feature_attr/img_feature_attr_module.ts":
/*!*********************************************************!*\
  !*** ./src/img_feature_attr/img_feature_attr_module.ts ***!
  \*********************************************************/
/*! exports provided: ImgFeatureAttrModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgFeatureAttrModule", function() { return ImgFeatureAttrModule; });
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/common.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/__ivy_ngcc__/fesm5/http.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/button.js");
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/expansion */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/expansion.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/input.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/select.js");
/* harmony import */ var _angular_material_slider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/slider */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/slider.js");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/radio */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/radio.js");
/* harmony import */ var _attr_histogram__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./attr_histogram */ "./src/img_feature_attr/attr_histogram.ts");
/* harmony import */ var _img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./img_feature_attr_viz */ "./src/img_feature_attr/img_feature_attr_viz.ts");














var ImgFeatureAttrModule = /** @class */ (function () {
    function ImgFeatureAttrModule() {
    }
    ImgFeatureAttrModule.ɵmod = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineNgModule"]({ type: ImgFeatureAttrModule });
    ImgFeatureAttrModule.ɵinj = _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵdefineInjector"]({ factory: function ImgFeatureAttrModule_Factory(t) { return new (t || ImgFeatureAttrModule)(); }, imports: [[
                _angular_common__WEBPACK_IMPORTED_MODULE_0__["CommonModule"],
                _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClientModule"],
                _angular_material_slider__WEBPACK_IMPORTED_MODULE_9__["MatSliderModule"],
                _angular_material_expansion__WEBPACK_IMPORTED_MODULE_5__["MatExpansionModule"],
                _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
                _angular_material_input__WEBPACK_IMPORTED_MODULE_7__["MatInputModule"],
                _angular_material_select__WEBPACK_IMPORTED_MODULE_8__["MatSelectModule"],
                _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__["MatFormFieldModule"],
                _angular_material_radio__WEBPACK_IMPORTED_MODULE_10__["MatRadioModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_3__["ReactiveFormsModule"],
            ]] });
    return ImgFeatureAttrModule;
}());

(function () { (typeof ngJitMode === "undefined" || ngJitMode) && _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵɵsetNgModuleScope"](ImgFeatureAttrModule, { declarations: [_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_12__["ImgFeatureAttrViz"], _attr_histogram__WEBPACK_IMPORTED_MODULE_11__["AttrHistogram"]], imports: [_angular_common__WEBPACK_IMPORTED_MODULE_0__["CommonModule"],
        _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClientModule"],
        _angular_material_slider__WEBPACK_IMPORTED_MODULE_9__["MatSliderModule"],
        _angular_material_expansion__WEBPACK_IMPORTED_MODULE_5__["MatExpansionModule"],
        _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
        _angular_material_input__WEBPACK_IMPORTED_MODULE_7__["MatInputModule"],
        _angular_material_select__WEBPACK_IMPORTED_MODULE_8__["MatSelectModule"],
        _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__["MatFormFieldModule"],
        _angular_material_radio__WEBPACK_IMPORTED_MODULE_10__["MatRadioModule"],
        _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
        _angular_forms__WEBPACK_IMPORTED_MODULE_3__["ReactiveFormsModule"]], exports: [_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_12__["ImgFeatureAttrViz"], _attr_histogram__WEBPACK_IMPORTED_MODULE_11__["AttrHistogram"]] }); })();
/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_2__["ɵsetClassMetadata"](ImgFeatureAttrModule, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"],
        args: [{
                imports: [
                    _angular_common__WEBPACK_IMPORTED_MODULE_0__["CommonModule"],
                    _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClientModule"],
                    _angular_material_slider__WEBPACK_IMPORTED_MODULE_9__["MatSliderModule"],
                    _angular_material_expansion__WEBPACK_IMPORTED_MODULE_5__["MatExpansionModule"],
                    _angular_material_button__WEBPACK_IMPORTED_MODULE_4__["MatButtonModule"],
                    _angular_material_input__WEBPACK_IMPORTED_MODULE_7__["MatInputModule"],
                    _angular_material_select__WEBPACK_IMPORTED_MODULE_8__["MatSelectModule"],
                    _angular_material_form_field__WEBPACK_IMPORTED_MODULE_6__["MatFormFieldModule"],
                    _angular_material_radio__WEBPACK_IMPORTED_MODULE_10__["MatRadioModule"],
                    _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormsModule"],
                    _angular_forms__WEBPACK_IMPORTED_MODULE_3__["ReactiveFormsModule"],
                ],
                declarations: [_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_12__["ImgFeatureAttrViz"], _attr_histogram__WEBPACK_IMPORTED_MODULE_11__["AttrHistogram"]],
                exports: [_img_feature_attr_viz__WEBPACK_IMPORTED_MODULE_12__["ImgFeatureAttrViz"], _attr_histogram__WEBPACK_IMPORTED_MODULE_11__["AttrHistogram"]]
            }]
    }], null, null); })();


/***/ }),

/***/ "./src/img_feature_attr/img_feature_attr_viz.ts":
/*!******************************************************!*\
  !*** ./src/img_feature_attr/img_feature_attr_viz.ts ***!
  \******************************************************/
/*! exports provided: ImgFeatureAttrViz */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImgFeatureAttrViz", function() { return ImgFeatureAttrViz; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _feature_attr_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./feature_attr_service */ "./src/img_feature_attr/feature_attr_service.ts");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/__ivy_ngcc__/fesm5/platform-browser.js");
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/expansion */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/expansion.js");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/radio */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/radio.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/__ivy_ngcc__/fesm5/forms.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/form-field.js");
/* harmony import */ var _angular_material_slider__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/slider */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/slider.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/input.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/__ivy_ngcc__/fesm5/button.js");














var _c0 = ["img_attr_canvas"];
/**
 * ImgFeatureAttrViz: A component to plot the original image, the significance
 * of each pixel, and overlay attributions with the original image.
 */
var ImgFeatureAttrViz = /** @class */ (function () {
    function ImgFeatureAttrViz(featureAttrService, domSanitizer) {
        this.featureAttrService = featureAttrService;
        this.domSanitizer = domSanitizer;
        this.imgExplanationSource = this.featureAttrService.imgExplanationSource;
        this.visualizationConfig = {
            type: 'pixels',
            overlay_multiplier: 0.4,
            clip_below_percentile: 35,
            clip_above_percentile: 99.9
        };
        this.postProcessors = ['pixels', 'outlines'];
        this.polarity = ['positive', 'negative', 'both'];
        this.overlay = ['none', 'grayscale', 'original'];
        this.panelOpenState = false;
        this.downloadData = this.domSanitizer.bypassSecurityTrustUrl('');
        // Handle on-destroy Subject, used to unsubscribe.
        this.destroyed = new rxjs__WEBPACK_IMPORTED_MODULE_2__["ReplaySubject"](1);
    }
    ImgFeatureAttrViz.prototype.ngAfterViewInit = function () {
        var _this = this;
        if (this.imgAttrCanvas) {
            var canvas_1 = this.imgAttrCanvas.nativeElement;
            var ctx_1 = this.imgAttrCanvas.nativeElement.getContext('2d');
            this.imgExplanationSource.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["takeUntil"])(this.destroyed))
                .subscribe(function (imgExplanation) {
                imgExplanation.updatePostProprocessedImageData();
                _this.visualizationConfig = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__assign"])({}, imgExplanation.visualizationConfig);
                var scale = 1;
                ctx_1.scale(scale, scale);
                var imageHeight = imgExplanation.imageHeight;
                var imageWidth = imgExplanation.imageWidth;
                var shift = imageWidth + 5;
                var imageTextSize = 12;
                // set canvase size
                canvas_1.width = imageWidth + 4 * shift;
                canvas_1.height = imageHeight + imageTextSize + 5;
                var imageData = imgExplanation.imageData;
                var posPostProcessedImageData = imgExplanation.posPostProcessedImageData;
                var negPostProcessedImageData = imgExplanation.negPostProcessedImageData;
                var halfOpacityImageData = imgExplanation.createImageData(imgExplanation.image3D, 1, imgExplanation.posPostProcessor.overlayMultiplier);
                var alpha = 1.0 - imgExplanation.posPostProcessor.overlayMultiplier;
                // draw image
                ctx_1.putImageData(imageData, 0, 0);
                // draw the post processed image
                ctx_1.putImageData(posPostProcessedImageData, shift, 0);
                // draw the image for overlaying
                ctx_1.putImageData(halfOpacityImageData, 2 * shift, 0);
                // draw the post processed image
                ctx_1.putImageData(negPostProcessedImageData, 3 * shift, 0);
                // draw the image for overlaying
                ctx_1.putImageData(halfOpacityImageData, 4 * shift, 0);
                // image labels
                ctx_1.font = imageTextSize + "px Arial";
                ctx_1.fillText('Original Image', 0, imageHeight + imageTextSize);
                ctx_1.fillText('Positive', shift, imageHeight + imageTextSize);
                ctx_1.fillText('Positive Overlay', shift * 2, imageHeight + imageTextSize);
                ctx_1.fillText('Negative', shift * 3, imageHeight + imageTextSize);
                ctx_1.fillText('Negative Overlay', shift * 4, imageHeight + imageTextSize);
                if (imgExplanation.posPostProcessor) {
                    for (var rIdx = 0; rIdx < imgExplanation.posPostProcessedImage.length; rIdx++) {
                        var row = imgExplanation.posPostProcessedImage[rIdx];
                        for (var cIdx = 0; cIdx < row.length; cIdx++) {
                            var cell = row[cIdx];
                            var fillStyle = "rgba(" + cell[0] + ", " + cell[1] + ", " + cell[2] + ", " + alpha + ")";
                            ctx_1.fillStyle = fillStyle;
                            ctx_1.fillRect(2 * shift + cIdx, rIdx, 1, 1);
                        }
                    }
                }
                if (imgExplanation.negPostProcessor) {
                    for (var rIdx = 0; rIdx < imgExplanation.negPostProcessedImage.length; rIdx++) {
                        var row = imgExplanation.negPostProcessedImage[rIdx];
                        for (var cIdx = 0; cIdx < row.length; cIdx++) {
                            var cell = row[cIdx];
                            var fillStyle = "rgba(" + cell[0] + ", " + cell[1] + ", " + cell[2] + ", " + alpha + ")";
                            ctx_1.fillStyle = fillStyle;
                            ctx_1.fillRect(4 * shift + cIdx, rIdx, 1, 1);
                        }
                    }
                }
                var iframeResizeEvent = new CustomEvent('iframeResizeEvent', { detail: document.documentElement.scrollHeight });
                window.parent.document.dispatchEvent(iframeResizeEvent);
            });
            var readyEvent = new CustomEvent('readyEvent', { detail: { ready: true } });
            window.parent.document.dispatchEvent(readyEvent);
        }
    };
    ImgFeatureAttrViz.prototype.ngOnDestroy = function () {
        // Unsubscribes all pending subscriptions.
        this.destroyed.next();
        this.destroyed.complete();
    };
    /** Notifies the service to update the attribution range accordingly. */
    ImgFeatureAttrViz.prototype.onClickUpdate = function () {
        this.featureAttrService.updatePostProcessor(this.visualizationConfig);
    };
    /** Saves current canvas as a png file for download. */
    ImgFeatureAttrViz.prototype.onClickDownload = function () {
        if (this.imgAttrCanvas) {
            var download = document.getElementById('download');
            var image = this.imgAttrCanvas.nativeElement.toDataURL('image/png')
                .replace('image/png', 'image/octet-stream');
            if (download) {
                this.downloadData = this.domSanitizer.bypassSecurityTrustUrl(image);
            }
        }
    };
    ImgFeatureAttrViz.ɵfac = function ImgFeatureAttrViz_Factory(t) { return new (t || ImgFeatureAttrViz)(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_feature_attr_service__WEBPACK_IMPORTED_MODULE_4__["FeatureAttrService"]), _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdirectiveInject"](_angular_platform_browser__WEBPACK_IMPORTED_MODULE_5__["DomSanitizer"])); };
    ImgFeatureAttrViz.ɵcmp = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵdefineComponent"]({ type: ImgFeatureAttrViz, selectors: [["app-img-feature-attr-viz"]], viewQuery: function ImgFeatureAttrViz_Query(rf, ctx) { if (rf & 1) {
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵviewQuery"](_c0, true);
        } if (rf & 2) {
            var _t;
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵqueryRefresh"](_t = _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵloadQuery"]()) && (ctx.imgAttrCanvas = _t.first);
        } }, decls: 45, vars: 9, consts: [[1, "block-title"], ["img_attr_canvas", ""], [3, "opened", "closed"], ["aria-label", "Select a post processor type", 3, "ngModel", "ngModelChange"], ["value", "pixels"], ["value", "outlines"], ["thumbLabel", "", "tickInterval", "0.1", "min", "0", "max", "1", "step", "0.1", 3, "value", "valueChange"], ["matInput", "", "type", "number", 3, "ngModel", "ngModelChange"], ["mat-raised-button", "", "id", "update-button", "color", "primary", 3, "click"], ["id", "download", "download", "canvas.png", 3, "href"], ["mat-raised-button", "", "id", "download-button", "color", "primary", 3, "click"]], template: function ImgFeatureAttrViz_Template(rf, ctx) { if (rf & 1) {
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](0, "div", 0);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](1, " Image Attributions\n");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](2, "canvas", null, 1);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](4, "mat-expansion-panel", 2);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("opened", function ImgFeatureAttrViz_Template_mat_expansion_panel_opened_4_listener() { return ctx.panelOpenState = true; })("closed", function ImgFeatureAttrViz_Template_mat_expansion_panel_closed_4_listener() { return ctx.panelOpenState = false; });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](5, "mat-expansion-panel-header");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](6, "mat-panel-title");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](7, " Visualization Configs ");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](8, "mat-panel-description");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](9);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelement"](10, "br");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](11, " Expand to change the configs ");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](12, "div");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](13, "h4");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](14, "Post Processor Type");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](15, "mat-radio-group", 3);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function ImgFeatureAttrViz_Template_mat_radio_group_ngModelChange_15_listener($event) { return ctx.visualizationConfig.type = $event; });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](16, "mat-radio-button", 4);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](17, "Pixels");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](18, "mat-radio-button", 5);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](19, "Outlines");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](20, "div");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](21, "h4");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](22, "Overlay Multiplier");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](23, "mat-label");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](24, "0");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](25, "mat-slider", 6);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("valueChange", function ImgFeatureAttrViz_Template_mat_slider_valueChange_25_listener($event) { return ctx.visualizationConfig.overlay_multiplier = $event; });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](26, "mat-label");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](27, "1");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](28, "div");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](29, "h4");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](30, "Clip Below Percentile & Clip Above Percentile");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](31, "mat-form-field");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](32, "mat-label");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](33, "clip below percentile");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](34, "input", 7);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function ImgFeatureAttrViz_Template_input_ngModelChange_34_listener($event) { return ctx.visualizationConfig.clip_below_percentile = $event; });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](35, "mat-form-field");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](36, "mat-label");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](37, "clip above percentile");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](38, "input", 7);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("ngModelChange", function ImgFeatureAttrViz_Template_input_ngModelChange_38_listener($event) { return ctx.visualizationConfig.clip_above_percentile = $event; });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](39, "button", 8);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function ImgFeatureAttrViz_Template_button_click_39_listener() { return ctx.onClickUpdate(); });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](40, "Update");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](41, "div");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](42, "a", 9);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementStart"](43, "button", 10);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵlistener"]("click", function ImgFeatureAttrViz_Template_button_click_43_listener() { return ctx.onClickDownload(); });
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtext"](44, "Download");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵelementEnd"]();
        } if (rf & 2) {
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](9);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵtextInterpolate4"](" Post processor type: ", ctx.visualizationConfig.type, " | Overlay multiplier: ", ctx.visualizationConfig.overlay_multiplier, " | Clip percentile range: [", ctx.visualizationConfig.clip_below_percentile, ", ", ctx.visualizationConfig.clip_above_percentile, "] ");
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](6);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.visualizationConfig.type);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](10);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("value", ctx.visualizationConfig.overlay_multiplier);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](9);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.visualizationConfig.clip_below_percentile);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](4);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("ngModel", ctx.visualizationConfig.clip_above_percentile);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵadvance"](4);
            _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵproperty"]("href", ctx.downloadData, _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵɵsanitizeUrl"]);
        } }, directives: [_angular_material_expansion__WEBPACK_IMPORTED_MODULE_6__["MatExpansionPanel"], _angular_material_expansion__WEBPACK_IMPORTED_MODULE_6__["MatExpansionPanelHeader"], _angular_material_expansion__WEBPACK_IMPORTED_MODULE_6__["MatExpansionPanelTitle"], _angular_material_expansion__WEBPACK_IMPORTED_MODULE_6__["MatExpansionPanelDescription"], _angular_material_radio__WEBPACK_IMPORTED_MODULE_7__["MatRadioGroup"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__["NgControlStatus"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__["NgModel"], _angular_material_radio__WEBPACK_IMPORTED_MODULE_7__["MatRadioButton"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__["MatLabel"], _angular_material_slider__WEBPACK_IMPORTED_MODULE_10__["MatSlider"], _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__["MatFormField"], _angular_material_input__WEBPACK_IMPORTED_MODULE_11__["MatInput"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__["NumberValueAccessor"], _angular_forms__WEBPACK_IMPORTED_MODULE_8__["DefaultValueAccessor"], _angular_material_button__WEBPACK_IMPORTED_MODULE_12__["MatButton"]], styles: [".block-title[_ngcontent-%COMP%] {\n  font-weight: 600;\n}\n\n.discription[_ngcontent-%COMP%] {\n  font-size: 10px;\n  color: \"#ccc\";\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi90bXAveGFpX2ltYWdlX3dpZGdldC94YWlfaW1hZ2Vfd2lkZ2V0L3dlYmFwcC9zcmMvaW1nX2ZlYXR1cmVfYXR0ci9pbWdfZmVhdHVyZV9hdHRyX3NoYXJlZF9zdHlsZS5zY3NzIiwic3JjL2ltZ19mZWF0dXJlX2F0dHIvaW1nX2ZlYXR1cmVfYXR0cl9zaGFyZWRfc3R5bGUuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGdCQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0VBQ0EsYUFBQTtBQ0NGIiwiZmlsZSI6InNyYy9pbWdfZmVhdHVyZV9hdHRyL2ltZ19mZWF0dXJlX2F0dHJfc2hhcmVkX3N0eWxlLnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuYmxvY2stdGl0bGUge1xuICBmb250LXdlaWdodDogNjAwO1xufVxuXG4uZGlzY3JpcHRpb24ge1xuICBmb250LXNpemU6IDEwcHg7XG4gIGNvbG9yOiAnI2NjYyc7XG59XG4iLCIuYmxvY2stdGl0bGUge1xuICBmb250LXdlaWdodDogNjAwO1xufVxuXG4uZGlzY3JpcHRpb24ge1xuICBmb250LXNpemU6IDEwcHg7XG4gIGNvbG9yOiBcIiNjY2NcIjtcbn0iXX0= */"] });
    return ImgFeatureAttrViz;
}());

/*@__PURE__*/ (function () { _angular_core__WEBPACK_IMPORTED_MODULE_1__["ɵsetClassMetadata"](ImgFeatureAttrViz, [{
        type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"],
        args: [{
                selector: 'app-img-feature-attr-viz',
                templateUrl: './img_feature_attr_viz.ng.html',
                styleUrls: [
                    './img_feature_attr_shared_style.scss',
                ]
            }]
    }], function () { return [{ type: _feature_attr_service__WEBPACK_IMPORTED_MODULE_4__["FeatureAttrService"] }, { type: _angular_platform_browser__WEBPACK_IMPORTED_MODULE_5__["DomSanitizer"] }]; }, { imgAttrCanvas: [{
            type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"],
            args: ['img_attr_canvas']
        }] }); })();


/***/ }),

/***/ "./src/img_feature_attr/outline_post_processor.ts":
/*!********************************************************!*\
  !*** ./src/img_feature_attr/outline_post_processor.ts ***!
  \********************************************************/
/*! exports provided: OutlinePostProcessor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OutlinePostProcessor", function() { return OutlinePostProcessor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _image_processing__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./image_processing */ "./src/img_feature_attr/image_processing.ts");
/* harmony import */ var _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./pixel_post_processor */ "./src/img_feature_attr/pixel_post_processor.ts");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/**
 * @fileoverview Outline post processor. This is a reimplementation in
 * TypeScript for
 * http://depot/google3/cloud/ml/explainability/explainers/post_processing/outline_attribution_processor.py
 */




// Any attribution above this value will be considered positive
// and anything below will be considered negative for the binarized
// mask obtained from the attribution image.
var BINARIZE_THRESHOLD = 0.001;
// Interior of shaded regions will be lighter than the border, by this
// factor. See draw_outlines() for details.
var SHADED_OUTLINES_WEIGHT = 0.3;
/**
 * OutlinePostProcessor
 */
var OutlinePostProcessor = /** @class */ (function (_super) {
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"])(OutlinePostProcessor, _super);
    function OutlinePostProcessor(polarity, clipAbovePercentile, clipBelowPercentile, overlayType, overlayMultiplier, shadeWithinOutlines, blurSigma, colormap, inputFeatureDomain) {
        if (polarity === void 0) { polarity = 'positive'; }
        if (clipAbovePercentile === void 0) { clipAbovePercentile = _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_clipAbovePercentile; }
        if (clipBelowPercentile === void 0) { clipBelowPercentile = _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_clipBelowPercentile; }
        if (overlayType === void 0) { overlayType = _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_OVERLAY_TYPE; }
        if (overlayMultiplier === void 0) { overlayMultiplier = _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].OVERLAY_MULTIPLIER; }
        if (shadeWithinOutlines === void 0) { shadeWithinOutlines = true; }
        if (blurSigma === void 0) { blurSigma = -1; }
        if (colormap === void 0) { colormap = _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_COLOR_MAP; }
        if (inputFeatureDomain === void 0) { inputFeatureDomain = {}; }
        var _this = _super.call(this, polarity, clipAbovePercentile, clipBelowPercentile, overlayType, overlayMultiplier, blurSigma, colormap, inputFeatureDomain) || this;
        _this.shadeWithinOutlines = shadeWithinOutlines;
        return _this;
    }
    /**
     * Creates an PixelPostProcessor instance from visualization config (which
     * is in json format) and input feature domain.
     */
    OutlinePostProcessor.fromDict = function (visualizationConfig, inputFeatureDomain) {
        if (inputFeatureDomain === void 0) { inputFeatureDomain = {}; }
        var _a, _b, _c, _d, _e, _f, _g, _h;
        var polarity = (_a = visualizationConfig.polarity, (_a !== null && _a !== void 0 ? _a : 'positive'));
        var clipAbovePercentile = (_b = visualizationConfig.clip_above_percentile, (_b !== null && _b !== void 0 ? _b : _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_clipAbovePercentile));
        var clipBelowPercentile = (_c = visualizationConfig.clip_below_percentile, (_c !== null && _c !== void 0 ? _c : _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_clipBelowPercentile));
        var overlayType = (_d = visualizationConfig.overlay_type, (_d !== null && _d !== void 0 ? _d : _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_OVERLAY_TYPE));
        var overlayMultiplier = (_e = visualizationConfig.overlay_multiplier, (_e !== null && _e !== void 0 ? _e : _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].OVERLAY_MULTIPLIER));
        var shadeWithinOutlines = (_f = visualizationConfig.shade_within_outlines, (_f !== null && _f !== void 0 ? _f : true));
        var blurSigma = (_g = visualizationConfig.blur_sigma, (_g !== null && _g !== void 0 ? _g : -1));
        var colormap = (_h = visualizationConfig.colormap, (_h !== null && _h !== void 0 ? _h : _pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["constants"].DEFAULT_COLOR_MAP));
        return new OutlinePostProcessor(polarity, clipAbovePercentile, clipBelowPercentile, overlayType, overlayMultiplier, shadeWithinOutlines, blurSigma, colormap, inputFeatureDomain);
    };
    /**
     * Extracts positive attributions from given attributions.
     * The attributions will be clipped to [low, high] percentiles and
     * and interpolated into [0, 255]
     */
    OutlinePostProcessor.prototype.getPositiveAttributions = function (attrs2D) {
        // Clip and scale attributions.
        var posAttrs = _super.prototype.getPositiveAttributions.call(this, attrs2D);
        // Draw outlines.
        var normalizedPosAttrs = posAttrs.map(function (row) { return row.map(function (val) { return val / 255.0; }); });
        var _a = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__read"])(this.getOutlines(normalizedPosAttrs), 2), border = _a[0], interior = _a[1];
        // Combine the border and shaded interior.
        var merged = border.map(function (row, rIdx) {
            return row.map(function (val, cIdx) {
                return val * 255.0 +
                    interior[rIdx][cIdx] * SHADED_OUTLINES_WEIGHT * 255.0;
            });
        });
        return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix"])(merged, 0, 255);
    };
    /**
     * Extracts negative attributions from given attributions.
     * The attributions will be clipped to [low, high] percentiles and
     * and interpolated into [0, 255]
     */
    OutlinePostProcessor.prototype.getNegativeAttributions = function (attrs2D) {
        // Clip and scale attributions.
        var negAttrs = _super.prototype.getNegativeAttributions.call(this, attrs2D);
        // Draw outlines.
        var normalizedNegAttrs = negAttrs.map(function (row) { return row.map(function (val) { return val / 255.0; }); });
        var _a = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__read"])(this.getOutlines(normalizedNegAttrs), 2), border = _a[0], interior = _a[1];
        // Combine the border and shaded interior.
        var merged = border.map(function (row, rIdx) {
            return row.map(function (val, cIdx) {
                return val * 255.0 +
                    interior[rIdx][cIdx] * SHADED_OUTLINES_WEIGHT * 255.0;
            });
        });
        return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix"])(merged, 0, 255);
    };
    OutlinePostProcessor.prototype.getOutlines = function (attrs2D, percentageConnectedComponentsToKeep, connectedComponentStructure) {
        var e_1, _a, e_2, _b, e_3, _c;
        if (percentageConnectedComponentsToKeep === void 0) { percentageConnectedComponentsToKeep = 90; }
        if (connectedComponentStructure === void 0) { connectedComponentStructure = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]; }
        var binaryAttrs = this.binarize(attrs2D);
        var filledHolesAttrs = Object(_image_processing__WEBPACK_IMPORTED_MODULE_1__["binaryHoleFilling"])(binaryAttrs);
        var indicesList = [];
        Object(_image_processing__WEBPACK_IMPORTED_MODULE_1__["labelConnectedComponents"])(filledHolesAttrs, indicesList);
        // Go through each connected component and sum up attributions of that
        // component.
        var totalSum = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["sum2D"])(filledHolesAttrs);
        var connectComponentSums = [];
        try {
            for (var indicesList_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(indicesList), indicesList_1_1 = indicesList_1.next(); !indicesList_1_1.done; indicesList_1_1 = indicesList_1.next()) {
                var cc = indicesList_1_1.value;
                var ccSum = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["sum"])(cc.map(function (_a) {
                    var _b = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__read"])(_a, 2), rIdx = _b[0], cIdx = _b[1];
                    return filledHolesAttrs[rIdx][cIdx];
                }));
                connectComponentSums.push(ccSum);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (indicesList_1_1 && !indicesList_1_1.done && (_a = indicesList_1.return)) _a.call(indicesList_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        // Compute the percentage of top components to keep.
        var ccIndices = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["range"])(indicesList.length);
        ccIndices.sort(function (a, b) {
            return connectComponentSums[b] - connectComponentSums[a];
        });
        var cumulativeSortedSums = [];
        var cumulativedSum = 0;
        try {
            for (var ccIndices_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(ccIndices), ccIndices_1_1 = ccIndices_1.next(); !ccIndices_1_1.done; ccIndices_1_1 = ccIndices_1.next()) {
                var idx = ccIndices_1_1.value;
                cumulativedSum += connectComponentSums[idx];
                cumulativeSortedSums.push(cumulativedSum);
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (ccIndices_1_1 && !ccIndices_1_1.done && (_b = ccIndices_1.return)) _b.call(ccIndices_1);
            }
            finally { if (e_2) throw e_2.error; }
        }
        var cutoffThreshold = (percentageConnectedComponentsToKeep * totalSum) / 100.0;
        var cutoffIdx = 0;
        while (cutoffIdx < 2 && cutoffIdx < cumulativeSortedSums.length &&
            cumulativeSortedSums[cutoffIdx] < cutoffThreshold) {
            cutoffIdx++;
        }
        var borderMask = attrs2D.map(function (row) { return row.map(function (val) { return 0; }); });
        for (var idx = 0; idx <= cutoffIdx && idx < cumulativeSortedSums.length; idx++) {
            var ccIdx = ccIndices[idx];
            try {
                for (var _d = (e_3 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(indicesList[ccIdx])), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var _f = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__read"])(_e.value, 2), rIdx = _f[0], cIdx = _f[1];
                    borderMask[rIdx][cIdx] = 1;
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_c = _d.return)) _c.call(_d);
                }
                finally { if (e_3) throw e_3.error; }
            }
        }
        var erodedMask = Object(_image_processing__WEBPACK_IMPORTED_MODULE_1__["binaryErosion"])(borderMask);
        var interiorMask = attrs2D.map(function (row) { return row.map(function (val) { return 0; }); });
        for (var rIdx = 0; rIdx < attrs2D.length; rIdx++) {
            for (var cIdx = 0; cIdx < attrs2D[rIdx].length; cIdx++) {
                if (erodedMask[rIdx][cIdx] === 1) {
                    borderMask[rIdx][cIdx] = 0;
                    interiorMask[rIdx][cIdx] = this.shadeWithinOutlines ? 1 : 0;
                }
            }
        }
        return [borderMask, interiorMask];
    };
    OutlinePostProcessor.prototype.binarize = function (attrs2D) {
        return attrs2D.map(function (row) {
            return row.map(function (val) { return ((val > BINARIZE_THRESHOLD) ? 1 : 0); });
        });
    };
    return OutlinePostProcessor;
}(_pixel_post_processor__WEBPACK_IMPORTED_MODULE_2__["PixelPostProcessor"]));



/***/ }),

/***/ "./src/img_feature_attr/pixel_post_processor.ts":
/*!******************************************************!*\
  !*** ./src/img_feature_attr/pixel_post_processor.ts ***!
  \******************************************************/
/*! exports provided: constants, PixelPostProcessor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "constants", function() { return constants; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PixelPostProcessor", function() { return PixelPostProcessor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _colors__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./colors */ "./src/img_feature_attr/colors.ts");
/* harmony import */ var _post_processor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./post_processor */ "./src/img_feature_attr/post_processor.ts");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/**
 * @fileoverview Pixel post processor. This is a reimplementation in TypeScript
 * for http://depot/google3/cloud/ml/explainability/explainers/post_processing/pixel_attribution_processor.py
 */




/**
 * A set of constants for pixel post processor
 */
var constants = {
    // RGB Projection vectors.
    GREEN: [0.0, 255.0, 0.0],
    RED: [255.0, 0.0, 0.0],
    // Default parameter values.
    DEFAULT_clipAbovePercentile: 99.9,
    DEFAULT_clipBelowPercentile: 35,
    DEFAULT_OVERLAY_TYPE: 'none',
    DEFAULT_MASK_OPACITY: 0.25,
    // While overlaying visualization over images, we multiply components with
    // a multiplier and add a constant bias, before clipping to range [0, 255].
    OVERLAY_MULTIPLIER: 0.4,
    OVERLAY_BIAS: 0.0,
    // Default color map.
    DEFAULT_COLOR_MAP: 'pink_green',
    // Valid properties
    VALID_POLARITY: ['positive', 'negative', 'both'],
    VALID_OVERLAY_TYPES: ['none', 'original', 'grayscale', 'mask_black'],
};
/**
 * PixelPostProcessor
 */
var PixelPostProcessor = /** @class */ (function (_super) {
    Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"])(PixelPostProcessor, _super);
    function PixelPostProcessor(polarity, clipAbovePercentile, clipBelowPercentile, overlayType, overlayMultiplier, blurSigma, colormap, inputFeatureDomain) {
        if (polarity === void 0) { polarity = 'positive'; }
        if (clipAbovePercentile === void 0) { clipAbovePercentile = constants.DEFAULT_clipAbovePercentile; }
        if (clipBelowPercentile === void 0) { clipBelowPercentile = constants.DEFAULT_clipBelowPercentile; }
        if (overlayType === void 0) { overlayType = constants.DEFAULT_OVERLAY_TYPE; }
        if (overlayMultiplier === void 0) { overlayMultiplier = constants.OVERLAY_MULTIPLIER; }
        if (blurSigma === void 0) { blurSigma = -1; }
        if (colormap === void 0) { colormap = constants.DEFAULT_COLOR_MAP; }
        if (inputFeatureDomain === void 0) { inputFeatureDomain = {}; }
        var _this = _super.call(this) || this;
        // Verifies if the given properties have valid values
        if (!constants.VALID_POLARITY.includes(polarity)) {
            throw new Error('Invalid polarity provided: ' + polarity);
        }
        if (!constants.VALID_OVERLAY_TYPES.includes(overlayType)) {
            throw new Error('Invalid overlay type provided: ' + overlayType);
        }
        if (overlayType === 'mask_black') {
            // Always use red-green for overlay type MASK_BLACK.
            colormap = constants.DEFAULT_COLOR_MAP;
        }
        _this.validateAttributionsPercentileRange(clipAbovePercentile, clipBelowPercentile);
        if (!(colormap in _colors__WEBPACK_IMPORTED_MODULE_1__["colors"].COLOR_MAPS)) {
            throw new Error("Invalid color map " + colormap + " provided. Must be one of " +
                ("" + Object.keys(_colors__WEBPACK_IMPORTED_MODULE_1__["colors"].COLOR_MAPS)));
        }
        _this.polarity = polarity;
        _this.clipAbovePercentile = clipAbovePercentile;
        _this.clipBelowPercentile = clipBelowPercentile;
        _this.overlayType = overlayType;
        _this.overlayMultiplier = overlayMultiplier;
        _this.blurSigma = blurSigma;
        _this.inputFeatureDomain = inputFeatureDomain;
        _this.colormap = colormap;
        _this.positiveColormap = _colors__WEBPACK_IMPORTED_MODULE_1__["colors"].COLOR_MAPS[_this.colormap]['positive'];
        _this.negativeColormap = _colors__WEBPACK_IMPORTED_MODULE_1__["colors"].COLOR_MAPS[_this.colormap]['negative'];
        return _this;
    }
    /**
     * Creates an PixelPostProcessor instance from visualization config (which
     * is in json format) and input feature domain.
     */
    PixelPostProcessor.fromDict = function (visualizationConfig, inputFeatureDomain) {
        if (inputFeatureDomain === void 0) { inputFeatureDomain = {}; }
        var _a, _b, _c, _d, _e, _f, _g;
        var polarity = (_a = visualizationConfig.polarity, (_a !== null && _a !== void 0 ? _a : 'positive'));
        var clipAbovePercentile = (_b = visualizationConfig.clip_above_percentile, (_b !== null && _b !== void 0 ? _b : constants.DEFAULT_clipAbovePercentile));
        var clipBelowPercentile = (_c = visualizationConfig.clip_below_percentile, (_c !== null && _c !== void 0 ? _c : constants.DEFAULT_clipBelowPercentile));
        var overlayType = (_d = visualizationConfig.overlay_type, (_d !== null && _d !== void 0 ? _d : constants.DEFAULT_OVERLAY_TYPE));
        var overlayMultiplier = (_e = visualizationConfig.overlay_multiplier, (_e !== null && _e !== void 0 ? _e : constants.OVERLAY_MULTIPLIER));
        var blurSigma = (_f = visualizationConfig.blur_sigma, (_f !== null && _f !== void 0 ? _f : -1));
        var colormap = (_g = visualizationConfig.colormap, (_g !== null && _g !== void 0 ? _g : constants.DEFAULT_COLOR_MAP));
        return new PixelPostProcessor(polarity, clipAbovePercentile, clipBelowPercentile, overlayType, overlayMultiplier, blurSigma, colormap, inputFeatureDomain);
    };
    /** Runs post processor steps to generate an post-processed image */
    PixelPostProcessor.prototype.process = function (attrs2D, image3D) {
        var _this = this;
        var attrsInRGB = this.convertAttrsToRGB(attrs2D);
        if (this.overlayType === 'none') {
            return attrsInRGB;
        }
        var normalizedImage = this.normalizeImage0To255(image3D, this.inputFeatureDomain);
        if (this.overlayType === 'mask_black') {
            var mask = attrsInRGB.map(function (row) { return row.map(function (cell) { return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(cell)); }); });
            var rgbMask = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["unflatten2Dto3D"])(mask, [1.0 / 255, 1.0 / 255, 1.0 / 255]);
            var rgbMaskShift = rgbMask.map(function (row) { return row.map(function (cell) { return cell.map(function (val) { return val + constants.DEFAULT_MASK_OPACITY; }); }); });
            var rgbMaskShiftClip_1 = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix3D"])(rgbMaskShift, constants.DEFAULT_MASK_OPACITY, 1);
            return normalizedImage.map(function (row, r) { return row.map(function (cell, c) { return cell.map(function (val, i) { return val + rgbMaskShiftClip_1[r][c][i]; }); }); });
        }
        var imageBackground = normalizedImage;
        if (this.overlayType === 'grayscale') {
            var grayscaleImage2D = imageBackground.map(function (row) { return row.map(function (cell) { return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["mean"])(cell); }); });
            imageBackground = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["unflatten2Dto3D"])(grayscaleImage2D, [1.0, 1.0, 1.0]);
        }
        var background = imageBackground.map(function (row) { return row.map(function (cell) { return cell.map(function (val) { return val * _this.overlayMultiplier; }); }); });
        var overlay = attrsInRGB.map(function (row) { return row.map(function (cell) { return cell.map(function (val) { return val * (1.0 - _this.overlayMultiplier); }); }); });
        var merged = background.map(function (row, r) { return row.map(function (cell, c) { return cell.map(function (val, i) {
            return val + overlay[r][c][i] + constants.OVERLAY_BIAS;
        }); }); });
        return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix3D"])(merged, 0, 255);
    };
    PixelPostProcessor.prototype.convertAttrsToRGB = function (attrs2D) {
        var _this = this;
        var posAttrs = this.getPositiveAttributions(attrs2D);
        var negAttrs = this.getNegativeAttributions(attrs2D);
        var attrRGBColors = [];
        if (this.polarity === 'both') {
            for (var r = 0; r < attrs2D.length; r++) {
                var newRow = [];
                for (var c = 0; c < attrs2D[0].length; c++) {
                    if (posAttrs[r][c] >= negAttrs[r][c]) {
                        var attrIdx = Math.floor(posAttrs[r][c]);
                        var attrColor = this.positiveColormap[attrIdx];
                        newRow.push(attrColor);
                    }
                    else {
                        var attrIdx = Math.floor(negAttrs[r][c]);
                        var attrColor = this.negativeColormap[attrIdx];
                        newRow.push(attrColor);
                    }
                }
                attrRGBColors.push(newRow);
            }
        }
        else if (this.polarity === 'positive') {
            attrRGBColors = posAttrs.map(function (row) { return row.map(function (val) { return _this.positiveColormap[Math.floor(val)]; }); });
        }
        else {
            attrRGBColors = negAttrs.map(function (row) { return row.map(function (val) { return _this.negativeColormap[Math.floor(val)]; }); });
        }
        return attrRGBColors;
    };
    /**
     * Extracts positive attributions from given attributions.
     * The attributions will be clipped to [low, high] percentiles and
     * and interpolated into [0, 255]
     */
    PixelPostProcessor.prototype.getPositiveAttributions = function (attrs2D) {
        var attrsMax = Math.max(0, Object(_utils__WEBPACK_IMPORTED_MODULE_3__["findMaxVal"])(attrs2D));
        // selects positive attributions.
        var clippedAttrs2D = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix"])(attrs2D, 0, attrsMax);
        var clippedAttrs1D = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["flatten2Dto1D"])(clippedAttrs2D);
        var low = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["derivePercentile"])(clippedAttrs1D, this.clipBelowPercentile);
        var high = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["derivePercentile"])(clippedAttrs1D, this.clipAbovePercentile);
        // clips to [low, high] and interpolates to [0, 255].
        return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["interpolate"])(clippedAttrs2D, [low, high], [0, 255]);
    };
    /**
     * Extracts negative attributions from given attributions.
     * The attributions will be clipped to [low, high] percentiles and
     * and interpolated into [0, 255]
     */
    PixelPostProcessor.prototype.getNegativeAttributions = function (attrs2D) {
        var attrsMin = Math.min(0, Object(_utils__WEBPACK_IMPORTED_MODULE_3__["findMinVal"])(attrs2D));
        // selects negative attributions.
        var clippedAttrs2D = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["clipMatrix"])(attrs2D, attrsMin, 0);
        // converts to absolute values
        var clippedAttrs2DAbs = clippedAttrs2D.map(function (row) { return row.map(function (val) { return Math.abs(val); }); });
        var clippedAttrs1D = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["flatten2Dto1D"])(clippedAttrs2DAbs);
        var low = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["derivePercentile"])(clippedAttrs1D, this.clipBelowPercentile);
        var high = Object(_utils__WEBPACK_IMPORTED_MODULE_3__["derivePercentile"])(clippedAttrs1D, this.clipAbovePercentile);
        // clips to [low, high] and interpolates to [0, 255].
        return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["interpolate"])(clippedAttrs2DAbs, [low, high], [0, 255]);
    };
    /**
     * Validates attributions_percentile_range, raises ValueError on failure.
     */
    PixelPostProcessor.prototype.validateAttributionsPercentileRange = function (clipAbovePercentile, clipBelowPercentile) {
        var e_1, _a;
        if (clipBelowPercentile >= clipAbovePercentile) {
            throw new Error('Invalid values for clipAbovePercentile, clipBelowPercentile: ' +
                ("(" + clipAbovePercentile + ", " + clipBelowPercentile + ")") +
                'clipBelowPercentile must be smaller than clipAbovePercentile.');
        }
        try {
            for (var _b = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])([clipAbovePercentile, clipBelowPercentile]), _c = _b.next(); !_c.done; _c = _b.next()) {
                var value = _c.value;
                var valueNumber = value;
                if (valueNumber < 0 || valueNumber > 100.0) {
                    throw new Error("Invalid value " + value + " provided for clipping attributions. " +
                        ("Value " + valueNumber + " is not in range [0, 100]."));
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
    };
    return PixelPostProcessor;
}(_post_processor__WEBPACK_IMPORTED_MODULE_2__["PostProcessor"]));



/***/ }),

/***/ "./src/img_feature_attr/post_processor.ts":
/*!************************************************!*\
  !*** ./src/img_feature_attr/post_processor.ts ***!
  \************************************************/
/*! exports provided: PostProcessor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PostProcessor", function() { return PostProcessor; });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./src/img_feature_attr/utils.ts");
/**
 * @fileoverview Base class for post processors.
 */

/**
 * Base class for post processors.
 */
var PostProcessor = /** @class */ (function () {
    function PostProcessor() {
    }
    /**
     * Normalizes the given image into [0, 255].
     * If the target domain is given, processes according to the config;
     * otherwise, infers an appropriate range.
     */
    PostProcessor.prototype.normalizeImage0To255 = function (values, domain) {
        if (domain === void 0) { domain = {}; }
        var _a, _b, _c, _d;
        // Case 1: mean/stddev based normalization.
        if (domain.hasOwnProperty('original_mean') &&
            domain.hasOwnProperty('original_stddev')) {
            var mean_1 = (_a = domain.original_mean, (_a !== null && _a !== void 0 ? _a : 0));
            var stddev_1 = (_b = domain.original_stddev, (_b !== null && _b !== void 0 ? _b : 1));
            return values.map(function (row) { return row.map(function (cell) { return cell.map(function (val) {
                var newVal = stddev_1 * val + mean_1;
                if (newVal < 0)
                    return 0;
                if (newVal > 255)
                    return 255;
                return newVal;
            }); }); });
        }
        // Case 2: scaling based normalization.
        var rangeMin = 0;
        var rangeMax = 1;
        if (domain.hasOwnProperty('max') && domain.hasOwnProperty('min')) {
            rangeMin = (_c = domain.min, (_c !== null && _c !== void 0 ? _c : 0));
            rangeMax = (_d = domain.max, (_d !== null && _d !== void 0 ? _d : 1));
        }
        var imageMax = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["findMaxVal3D"])(values, false);
        var imageMin = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["findMinVal3D"])(values, false);
        if (-1 <= imageMin && imageMin < 0 && imageMax <= 1) {
            rangeMin = -1;
            rangeMax = 1;
        }
        else if (0 <= imageMin && 1 < imageMax && imageMax <= 255) {
            rangeMin = 0;
            rangeMax = 255;
        }
        if (imageMin < rangeMin || rangeMax < imageMax) {
            throw new Error('Image values are not in the specified feature domain.\n' +
                'Please check if the explanation metadata has a wrong input domain.');
        }
        return values.map(function (row) { return row.map(function (cell) { return cell.map(function (val) { return 255 * (val - rangeMin) / (rangeMax - rangeMin); }); }); });
    };
    return PostProcessor;
}());



/***/ }),

/***/ "./src/img_feature_attr/utils.ts":
/*!***************************************!*\
  !*** ./src/img_feature_attr/utils.ts ***!
  \***************************************/
/*! exports provided: range, range2, findMaxVal, findMinVal, findMaxVal3D, findMinVal3D, derivePercentile, clipMatrix, clipMatrix3D, flatten3Dto2D, flatten2Dto1D, unflatten2Dto3D, interpolate, binarySearch, sum, sum2D, mean, count2D, mean2D, var2D, std2D, count3D, sum3D, mean3D, var3D, std3D, isArray2D, isArray3D, logicNotArray2D */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "range", function() { return range; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "range2", function() { return range2; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findMaxVal", function() { return findMaxVal; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findMinVal", function() { return findMinVal; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findMaxVal3D", function() { return findMaxVal3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findMinVal3D", function() { return findMinVal3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "derivePercentile", function() { return derivePercentile; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clipMatrix", function() { return clipMatrix; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clipMatrix3D", function() { return clipMatrix3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "flatten3Dto2D", function() { return flatten3Dto2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "flatten2Dto1D", function() { return flatten2Dto1D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "unflatten2Dto3D", function() { return unflatten2Dto3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "interpolate", function() { return interpolate; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "binarySearch", function() { return binarySearch; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sum", function() { return sum; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sum2D", function() { return sum2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mean", function() { return mean; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "count2D", function() { return count2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mean2D", function() { return mean2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "var2D", function() { return var2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "std2D", function() { return std2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "count3D", function() { return count3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sum3D", function() { return sum3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mean3D", function() { return mean3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "var3D", function() { return var3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "std3D", function() { return std3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isArray2D", function() { return isArray2D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isArray3D", function() { return isArray3D; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "logicNotArray2D", function() { return logicNotArray2D; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/**
 * @fileoverview Utils for handling arrays and matrix.
 * These functions are mostly mimicking necessary numpy functionalities for
 * post processors.
 */

/**
 * Helper functions for mimicking Python's range().
 */
var range = function (n) {
    return Array.from({ length: n }).fill(0).map(function (v, i) { return i; });
};
/**
 * Helper functions for mimicking Python's range(start, end).
 */
var range2 = function (st, ed) {
    var n = ed - st;
    if (n <= 0) {
        return [];
    }
    return Array.from({ length: n }).fill(0).map(function (v, i) { return i + st; });
};
/**
 * Find the maximum absolute value in a matrix.
 */
function findMaxVal(matrix) {
    // Leverage map and Math.max plus spread operator to find max of each row
    var maxOfEachRow = matrix.map(function (row) { return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(row)); });
    // Then find the maximum of the maximums
    return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(maxOfEachRow));
}
/**
 * Find the minimum absolute value in a matrix.
 */
function findMinVal(matrix) {
    // Leverage map and Math.min plus spread operator to find min of each row
    var minOfEachRow = matrix.map(function (row) { return Math.min.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(row)); });
    // Then find the minimum of the minimums
    return Math.min.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(minOfEachRow));
}
/**
 * Find the max absolute value in a 3D matrix.
 */
function findMaxVal3D(matrix, flatten) {
    if (flatten === void 0) { flatten = true; }
    // Leverage map and Math.max plus spread operator to find max of each row
    var maxOfEachRow = matrix.map(function (row) {
        var cells = row.map(function (cell) {
            if (flatten) {
                return sum(cell);
            }
            return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(cell));
        });
        return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(cells));
    });
    // Then find the maximum of the maximums
    return Math.max.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(maxOfEachRow));
}
/**
 * Find the min absolute value in a 3D matrix.
 */
function findMinVal3D(matrix, flatten) {
    if (flatten === void 0) { flatten = true; }
    // Leverage map and Math.min plus spread operator to find min of each row
    var minOfEachRow = matrix.map(function (row) {
        var cells = row.map(function (cell) {
            if (flatten) {
                return sum(cell);
            }
            return Math.min.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(cell));
        });
        return Math.min.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(cells));
    });
    // Then find the minimum of the minimums
    return Math.min.apply(Math, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(minOfEachRow));
}
/**
 * Comparison function for sorting. The default sorting comparison function
 * will leave to floating point overflow/underflow in our use cases.
 */
function compare(a, b) {
    if (a < b) {
        return -1;
    }
    else if (a > b) {
        return 1;
    }
    return 0;
}
/**
 * Derive the given percentile value of an array.
 */
function derivePercentile(array, percentile) {
    var count = array.length;
    if (count === 0) {
        return -1;
    }
    var sortedArray = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__spread"])(array).sort(compare);
    var indexDouble = (percentile / 100.0) * (sortedArray.length - 1);
    var indexInteger = Math.floor(indexDouble);
    var fraction = indexDouble - indexInteger;
    if (Number.isInteger(indexDouble)) {
        return sortedArray[indexInteger];
    }
    else {
        return sortedArray[indexInteger] +
            fraction * (sortedArray[indexInteger + 1] - sortedArray[indexInteger]);
    }
}
/** Cilps a 2D array to make the values sits within [lowerBound, upperBound]. */
function clipMatrix(matrix, lowerBound, upperBound) {
    return matrix.map(function (row) { return row.map(function (val) {
        if (val < lowerBound)
            return lowerBound;
        if (val > upperBound)
            return upperBound;
        return val;
    }); });
}
/** Cilps a 3D array to make the values sits within [lowerBound, upperBound]. */
function clipMatrix3D(matrix, lowerBound, upperBound) {
    return matrix.map(function (row) { return row.map(function (cell) { return cell.map(function (val) {
        if (val < lowerBound)
            return lowerBound;
        if (val > upperBound)
            return upperBound;
        return val;
    }); }); });
}
/**
 * Flattens an 3D array to 2D.
 * If bySum is true, aggregates the innest dimension by sum; otherwise,
 * aggregates the dimension by average.
 */
function flatten3Dto2D(values, bySum) {
    var e_1, _a, e_2, _b;
    if (bySum === void 0) { bySum = false; }
    var mappedValues = [];
    try {
        for (var values_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(values), values_1_1 = values_1.next(); !values_1_1.done; values_1_1 = values_1.next()) {
            var row = values_1_1.value;
            var newRow = [];
            try {
                for (var row_1 = (e_2 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(row)), row_1_1 = row_1.next(); !row_1_1.done; row_1_1 = row_1.next()) {
                    var cell = row_1_1.value;
                    var newVal = void 0;
                    if (bySum) {
                        newVal = sum(cell);
                    }
                    else {
                        newVal = sum(cell) / cell.length;
                    }
                    newRow.push(newVal);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (row_1_1 && !row_1_1.done && (_b = row_1.return)) _b.call(row_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
            mappedValues.push(newRow);
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (values_1_1 && !values_1_1.done && (_a = values_1.return)) _a.call(values_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return mappedValues;
}
/** Flattens an 2D array to 1D */
function flatten2Dto1D(values) {
    var e_3, _a, e_4, _b;
    var mappedValues = [];
    try {
        for (var values_2 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(values), values_2_1 = values_2.next(); !values_2_1.done; values_2_1 = values_2.next()) {
            var row = values_2_1.value;
            try {
                for (var row_2 = (e_4 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(row)), row_2_1 = row_2.next(); !row_2_1.done; row_2_1 = row_2.next()) {
                    var cell = row_2_1.value;
                    mappedValues.push(cell);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (row_2_1 && !row_2_1.done && (_b = row_2.return)) _b.call(row_2);
                }
                finally { if (e_4) throw e_4.error; }
            }
        }
    }
    catch (e_3_1) { e_3 = { error: e_3_1 }; }
    finally {
        try {
            if (values_2_1 && !values_2_1.done && (_a = values_2.return)) _a.call(values_2);
        }
        finally { if (e_3) throw e_3.error; }
    }
    return mappedValues;
}
/** Projects an 2D arry to 3D */
function unflatten2Dto3D(values, rgbProjectionVector) {
    var e_5, _a, e_6, _b, e_7, _c;
    var mappedValues = [];
    try {
        for (var values_3 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(values), values_3_1 = values_3.next(); !values_3_1.done; values_3_1 = values_3.next()) {
            var row = values_3_1.value;
            var newRow = [];
            try {
                for (var row_3 = (e_6 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(row)), row_3_1 = row_3.next(); !row_3_1.done; row_3_1 = row_3.next()) {
                    var val = row_3_1.value;
                    var cell = [];
                    try {
                        for (var rgbProjectionVector_1 = (e_7 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(rgbProjectionVector)), rgbProjectionVector_1_1 = rgbProjectionVector_1.next(); !rgbProjectionVector_1_1.done; rgbProjectionVector_1_1 = rgbProjectionVector_1.next()) {
                            var projectVal = rgbProjectionVector_1_1.value;
                            cell.push(val * projectVal);
                        }
                    }
                    catch (e_7_1) { e_7 = { error: e_7_1 }; }
                    finally {
                        try {
                            if (rgbProjectionVector_1_1 && !rgbProjectionVector_1_1.done && (_c = rgbProjectionVector_1.return)) _c.call(rgbProjectionVector_1);
                        }
                        finally { if (e_7) throw e_7.error; }
                    }
                    newRow.push(cell);
                }
            }
            catch (e_6_1) { e_6 = { error: e_6_1 }; }
            finally {
                try {
                    if (row_3_1 && !row_3_1.done && (_b = row_3.return)) _b.call(row_3);
                }
                finally { if (e_6) throw e_6.error; }
            }
            mappedValues.push(newRow);
        }
    }
    catch (e_5_1) { e_5 = { error: e_5_1 }; }
    finally {
        try {
            if (values_3_1 && !values_3_1.done && (_a = values_3.return)) _a.call(values_3);
        }
        finally { if (e_5) throw e_5.error; }
    }
    return mappedValues;
}
/**
 * Interpolates the matrix from domain to range
 */
function interpolate(matrix, domain, range) {
    var e_8, _a, e_9, _b;
    domain.sort();
    range.sort();
    var mappedValues = [];
    try {
        for (var matrix_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(matrix), matrix_1_1 = matrix_1.next(); !matrix_1_1.done; matrix_1_1 = matrix_1.next()) {
            var row = matrix_1_1.value;
            var newRow = [];
            try {
                for (var row_4 = (e_9 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(row)), row_4_1 = row_4.next(); !row_4_1.done; row_4_1 = row_4.next()) {
                    var val = row_4_1.value;
                    // clips to domain upper bound and lower bound
                    var newVal = Math.max(val, domain[0]);
                    newVal = Math.min(newVal, domain[domain.length - 1]);
                    var idx = binarySearch(domain, newVal);
                    if (domain[idx] === newVal) {
                        // Case 1: exact mapping
                        newVal = range[idx];
                    }
                    else {
                        // Case 2: interpolating
                        //     newVal - domain[idx]
                        // ---------------------------- * (range[idx+1] - range[idx]) + range[idx]
                        //  domain[idx+1] - domain[idx]
                        var ratio = (newVal - domain[idx]) / (domain[idx + 1] - domain[idx]);
                        newVal = range[idx] + ratio * (range[idx + 1] - range[idx]);
                    }
                    newRow.push(newVal);
                }
            }
            catch (e_9_1) { e_9 = { error: e_9_1 }; }
            finally {
                try {
                    if (row_4_1 && !row_4_1.done && (_b = row_4.return)) _b.call(row_4);
                }
                finally { if (e_9) throw e_9.error; }
            }
            mappedValues.push(newRow);
        }
    }
    catch (e_8_1) { e_8 = { error: e_8_1 }; }
    finally {
        try {
            if (matrix_1_1 && !matrix_1_1.done && (_a = matrix_1.return)) _a.call(matrix_1);
        }
        finally { if (e_8) throw e_8.error; }
    }
    return mappedValues;
}
/**
 * Returns the index of the searching target using Binary Search.
 * When there are duplicated numbers, returns the leftmost index of the matches;
 * when there is no matching element, returns the rightmost index of the
 * elements that are smaller than target.
 *
 * When the searching target is smaller than the leftest element, returns -1.
 *
 * The given array has to be sorted.
 */
function binarySearch(sortedArray, tar) {
    var left = 0;
    var right = sortedArray.length - 1;
    var mid;
    var res = -1;
    while (left <= right) {
        mid = left + Math.floor((right - left) / 2);
        if (sortedArray[mid] === tar) {
            res = mid;
            right = mid - 1; // continue search in case there are duplicated numbers
        }
        else if (sortedArray[mid] < tar) {
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
    }
    if (res !== -1) {
        return res; // returns leftmost index of the target
    }
    // returns the index of the rightest element t where t < tar
    return right;
}
/** Returns sum of the give array. */
function sum(array) {
    var reducer = function (acc, cur) { return acc + cur; };
    return array.reduce(reducer);
}
/** Returns sum of the give 2D array. */
function sum2D(array2D) {
    return sum(array2D.map(function (row) { return sum(row); }));
}
/** Returns mean of the give array. Returns 0 for empty array. */
function mean(array) {
    if (array.length === 0)
        return 0;
    return sum(array) / array.length;
}
/** Returns count of the give 2D array. */
function count2D(array2D) {
    return sum(array2D.map(function (row) { return row.length; }));
}
/** Returns mean of the give 2D array. Returns 0 for empty array. */
function mean2D(array2D) {
    var count = count2D(array2D);
    return (count > 0) ? sum2D(array2D) / count : 0;
}
/** Returns variance of the give 2D array. Returns 0 for empty array. */
function var2D(array2D) {
    var count = count2D(array2D);
    if (count === 0) {
        return 0;
    }
    var avg = mean2D(array2D);
    var variance = sum(array2D.map(function (row) { return sum(row.map(function (val) { return (val - avg) * (val - avg); })); })) /
        count;
    return variance;
}
/** Returns std of the give 2D array. Returns 0 for empty array. */
function std2D(array2D) {
    var count = count2D(array2D);
    if (count === 0) {
        return 0;
    }
    return Math.sqrt(var2D(array2D));
}
/** Returns count of the give 3D array. */
function count3D(array3D) {
    return sum(array3D.map(function (row) { return sum(row.map(function (cell) { return cell.length; })); }));
}
/** Returns sum of the give 2D array. */
function sum3D(array3D) {
    return sum(array3D.map(function (row) { return sum(row.map(function (cell) { return sum(cell); })); }));
}
/** Returns mean of the give 3D array. Returns 0 for empty array. */
function mean3D(array3D) {
    var count = count3D(array3D);
    return (count > 0) ? sum3D(array3D) / count : 0;
}
/** Returns variance of the give 3D array. Returns 0 for empty array. */
function var3D(array3D) {
    var count = count3D(array3D);
    if (count === 0) {
        return 0;
    }
    var avg = mean3D(array3D);
    var variance = sum(array3D.map(function (row) { return sum(row.map(function (cell) { return sum(cell.map(function (val) { return (val - avg) * (val - avg); })); })); })) /
        count;
    return variance;
}
/** Returns std of the give 3D array. Returns 0 for empty array. */
function std3D(array3D) {
    var count = count3D(array3D);
    if (count === 0) {
        return 0;
    }
    return Math.sqrt(var3D(array3D));
}
/** Typeguard for Array2D */
function isArray2D(array) {
    return Array.isArray(array) && array.length > 0 && Array.isArray(array[0]) &&
        array[0].length > 0 && !Array.isArray(array[0][0]);
}
/** Typeguard for Array3D */
function isArray3D(array) {
    return Array.isArray(array) && array.length > 0 && Array.isArray(array[0]) &&
        array[0].length > 0 && Array.isArray(array[0][0]) &&
        array[0][0].length > 0 && !Array.isArray(array[0][0][0]);
}
/** Logic Not for a 2D array. */
function logicNotArray2D(array2D, inplace) {
    var e_10, _a, e_11, _b;
    if (inplace === void 0) { inplace = false; }
    var results = [];
    try {
        for (var array2D_1 = Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(array2D), array2D_1_1 = array2D_1.next(); !array2D_1_1.done; array2D_1_1 = array2D_1.next()) {
            var row = array2D_1_1.value;
            var newRow = [];
            try {
                for (var row_5 = (e_11 = void 0, Object(tslib__WEBPACK_IMPORTED_MODULE_0__["__values"])(row)), row_5_1 = row_5.next(); !row_5_1.done; row_5_1 = row_5.next()) {
                    var val = row_5_1.value;
                    newRow.push(val !== 0 ? 0 : 1);
                }
            }
            catch (e_11_1) { e_11 = { error: e_11_1 }; }
            finally {
                try {
                    if (row_5_1 && !row_5_1.done && (_b = row_5.return)) _b.call(row_5);
                }
                finally { if (e_11) throw e_11.error; }
            }
            results.push(newRow);
        }
    }
    catch (e_10_1) { e_10 = { error: e_10_1 }; }
    finally {
        try {
            if (array2D_1_1 && !array2D_1_1.done && (_a = array2D_1.return)) _a.call(array2D_1);
        }
        finally { if (e_10) throw e_10.error; }
    }
    if (inplace) {
        for (var r = 0; r < array2D.length; r++) {
            for (var c = 0; c < array2D[0].length; c++) {
                array2D[r][c] = results[r][c];
            }
        }
        results = array2D;
    }
    return results;
}


/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/__ivy_ngcc__/fesm5/core.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app/app_module */ "./src/app/app_module.ts");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/__ivy_ngcc__/fesm5/platform-browser.js");




if (_environments_environment__WEBPACK_IMPORTED_MODULE_1__["environment"].production)
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["enableProdMode"])();
_angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__["platformBrowser"]().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_2__["AppModule"])
    .catch(function (err) { return console.error(err); });
;


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /tmp/xai_image_widget/xai_image_widget/webapp/src/main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
