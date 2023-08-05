Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var panels_1 = require("app/components/panels");
var histogramQuery_1 = tslib_1.__importDefault(require("app/utils/performance/histogram/histogramQuery"));
var constants_1 = require("app/utils/performance/vitals/constants");
var vitalsCardsDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
var queryString_1 = require("app/utils/queryString");
var constants_2 = require("./constants");
var vitalCard_1 = tslib_1.__importDefault(require("./vitalCard"));
var VitalsPanel = /** @class */ (function (_super) {
    tslib_1.__extends(VitalsPanel, _super);
    function VitalsPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    VitalsPanel.prototype.renderVitalCard = function (vital, isLoading, error, data, histogram, color, min, max, precision) {
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitalDetails = constants_1.WEB_VITAL_DETAILS[vital];
        var zoomed = min !== undefined || max !== undefined;
        return (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={constants_2.NUM_BUCKETS} fields={zoomed ? [vital] : []} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (results) {
                var _a, _b;
                var loading = zoomed ? results.isLoading : isLoading;
                var errored = zoomed ? results.error !== null : error;
                var chartData = zoomed ? (_b = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : histogram : histogram;
                return (<vitalCard_1.default location={location} isLoading={loading} error={errored} vital={vital} vitalDetails={vitalDetails} summaryData={data} chartData={chartData} colors={color} eventView={eventView} organization={organization} min={min} max={max} precision={precision} dataFilter={dataFilter}/>);
            }}
      </histogramQuery_1.default>);
    };
    VitalsPanel.prototype.renderVitalGroup = function (group, summaryResults) {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitals = group.vitals, colors = group.colors, min = group.min, max = group.max, precision = group.precision;
        var bounds = vitals.reduce(function (allBounds, vital) {
            var slug = constants_1.WEB_VITAL_DETAILS[vital].slug;
            allBounds[vital] = {
                start: queryString_1.decodeScalar(location.query[slug + "Start"]),
                end: queryString_1.decodeScalar(location.query[slug + "End"]),
            };
            return allBounds;
        }, {});
        return (<histogramQuery_1.default location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={constants_2.NUM_BUCKETS} fields={vitals} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (multiHistogramResults) {
                var isLoading = summaryResults.isLoading || multiHistogramResults.isLoading;
                var error = summaryResults.error !== null || multiHistogramResults.error !== null;
                return (<react_1.Fragment>
              {vitals.map(function (vital, index) {
                        var _a, _b, _c, _d, _e;
                        var data = (_b = (_a = summaryResults === null || summaryResults === void 0 ? void 0 : summaryResults.vitalsData) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : null;
                        var histogram = (_d = (_c = multiHistogramResults.histograms) === null || _c === void 0 ? void 0 : _c[vital]) !== null && _d !== void 0 ? _d : [];
                        var _f = (_e = bounds[vital]) !== null && _e !== void 0 ? _e : {}, start = _f.start, end = _f.end;
                        return (<react_1.Fragment key={vital}>
                    {_this.renderVitalCard(vital, isLoading, error, data, histogram, [colors[index]], parseBound(start, precision), parseBound(end, precision), precision)}
                  </react_1.Fragment>);
                    })}
            </react_1.Fragment>);
            }}
      </histogramQuery_1.default>);
    };
    VitalsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView;
        var allVitals = constants_2.VITAL_GROUPS.reduce(function (keys, _a) {
            var vitals = _a.vitals;
            return keys.concat(vitals);
        }, []);
        return (<panels_1.Panel>
        <vitalsCardsDiscoverQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} vitals={allVitals}>
          {function (results) { return (<react_1.Fragment>
              {constants_2.VITAL_GROUPS.map(function (vitalGroup) { return (<react_1.Fragment key={vitalGroup.vitals.join('')}>
                  {_this.renderVitalGroup(vitalGroup, results)}
                </react_1.Fragment>); })}
            </react_1.Fragment>); }}
        </vitalsCardsDiscoverQuery_1.default>
      </panels_1.Panel>);
    };
    return VitalsPanel;
}(react_1.Component));
function parseBound(boundString, precision) {
    if (boundString === undefined) {
        return undefined;
    }
    else if (precision === undefined || precision === 0) {
        return parseInt(boundString, 10);
    }
    return parseFloat(boundString);
}
exports.default = VitalsPanel;
//# sourceMappingURL=vitalsPanel.jsx.map