Object.defineProperty(exports, "__esModule", { value: true });
exports.removeHistogramQueryStrings = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var queryString_1 = require("app/utils/queryString");
var constants_1 = require("./constants");
var Histogram = /** @class */ (function (_super) {
    tslib_1.__extends(Histogram, _super);
    function Histogram() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleResetView = function () {
            var _a = _this.props, location = _a.location, zoomKeys = _a.zoomKeys;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: removeHistogramQueryStrings(location, zoomKeys),
            });
        };
        _this.handleFilterChange = function (value) {
            var _a = _this.props, location = _a.location, zoomKeys = _a.zoomKeys;
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, removeHistogramQueryStrings(location, zoomKeys)), { dataFilter: value }),
            });
        };
        return _this;
    }
    Histogram.prototype.isZoomed = function () {
        var _a = this.props, location = _a.location, zoomKeys = _a.zoomKeys;
        return zoomKeys.map(function (key) { return location.query[key]; }).some(function (value) { return value !== undefined; });
    };
    Histogram.prototype.getActiveFilter = function () {
        var location = this.props.location;
        var dataFilter = location.query.dataFilter
            ? queryString_1.decodeScalar(location.query.dataFilter)
            : constants_1.FILTER_OPTIONS[0].value;
        return constants_1.FILTER_OPTIONS.find(function (item) { return item.value === dataFilter; }) || constants_1.FILTER_OPTIONS[0];
    };
    Histogram.prototype.render = function () {
        var childrenProps = {
            isZoomed: this.isZoomed(),
            handleResetView: this.handleResetView,
            activeFilter: this.getActiveFilter(),
            handleFilterChange: this.handleFilterChange,
            filterOptions: constants_1.FILTER_OPTIONS,
        };
        return this.props.children(childrenProps);
    };
    return Histogram;
}(React.Component));
function removeHistogramQueryStrings(location, zoomKeys) {
    var query = tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined });
    delete query.dataFilter;
    // reset all zoom parameters
    zoomKeys.forEach(function (key) { return delete query[key]; });
    return query;
}
exports.removeHistogramQueryStrings = removeHistogramQueryStrings;
exports.default = Histogram;
//# sourceMappingURL=index.jsx.map