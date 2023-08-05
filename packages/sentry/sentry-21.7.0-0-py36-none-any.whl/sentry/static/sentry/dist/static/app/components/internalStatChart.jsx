Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var InternalStatChart = /** @class */ (function (_super) {
    tslib_1.__extends(InternalStatChart, _super);
    function InternalStatChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: true,
            data: null,
        };
        _this.fetchData = function () {
            _this.setState({ loading: true });
            _this.props.api.request('/internal/stats/', {
                method: 'GET',
                data: {
                    since: _this.props.since,
                    resolution: _this.props.resolution,
                    key: _this.props.stat,
                },
                success: function (data) {
                    return _this.setState({
                        data: data,
                        loading: false,
                        error: false,
                    });
                },
                error: function () { return _this.setState({ error: true, loading: false }); },
            });
        };
        return _this;
    }
    InternalStatChart.prototype.componentDidMount = function () {
        this.fetchData();
    };
    InternalStatChart.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.loading !== nextState.loading;
    };
    InternalStatChart.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.since !== this.props.since ||
            prevProps.stat !== this.props.stat ||
            prevProps.resolution !== this.props.resolution) {
            this.fetchData();
        }
    };
    InternalStatChart.prototype.render = function () {
        var _a;
        var _b = this.state, loading = _b.loading, error = _b.error, data = _b.data;
        var _c = this.props, label = _c.label, height = _c.height;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        else if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        var series = {
            seriesName: label,
            data: (_a = data === null || data === void 0 ? void 0 : data.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
                return ({
                    name: timestamp * 1000,
                    value: value,
                });
            })) !== null && _a !== void 0 ? _a : [],
        };
        return (<miniBarChart_1.default height={height !== null && height !== void 0 ? height : 150} series={[series]} isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    };
    return InternalStatChart;
}(react_1.Component));
exports.default = withApi_1.default(InternalStatChart);
//# sourceMappingURL=internalStatChart.jsx.map