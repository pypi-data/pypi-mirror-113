Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var deviceName_1 = require("app/components/deviceName");
var tagDistributionMeter_1 = tslib_1.__importDefault(require("app/components/tagDistributionMeter"));
var GroupTagDistributionMeter = /** @class */ (function (_super) {
    tslib_1.__extends(GroupTagDistributionMeter, _super);
    function GroupTagDistributionMeter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
        };
        return _this;
    }
    GroupTagDistributionMeter.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupTagDistributionMeter.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return (this.state.loading !== nextState.loading ||
            this.state.error !== nextState.error ||
            this.props.tag !== nextProps.tag ||
            this.props.name !== nextProps.name ||
            this.props.totalValues !== nextProps.totalValues ||
            this.props.topValues !== nextProps.topValues);
    };
    GroupTagDistributionMeter.prototype.fetchData = function () {
        var _this = this;
        this.setState({
            loading: true,
            error: false,
        });
        deviceName_1.loadDeviceListModule()
            .then(function (iOSDeviceList) {
            _this.setState({
                iOSDeviceList: iOSDeviceList,
                error: false,
                loading: false,
            });
        })
            .catch(function () {
            _this.setState({
                error: true,
                loading: false,
            });
        });
    };
    GroupTagDistributionMeter.prototype.render = function () {
        var _a = this.props, organization = _a.organization, group = _a.group, tag = _a.tag, totalValues = _a.totalValues, topValues = _a.topValues;
        var _b = this.state, loading = _b.loading, error = _b.error, iOSDeviceList = _b.iOSDeviceList;
        var url = "/organizations/" + organization.slug + "/issues/" + group.id + "/tags/" + tag + "/";
        var segments = topValues
            ? topValues.map(function (value) { return (tslib_1.__assign(tslib_1.__assign({}, value), { name: iOSDeviceList
                    ? deviceName_1.deviceNameMapper(value.name || '', iOSDeviceList) || ''
                    : value.name, url: url })); })
            : [];
        return (<tagDistributionMeter_1.default title={tag} totalValues={totalValues} isLoading={loading} hasError={error} segments={segments}/>);
    };
    return GroupTagDistributionMeter;
}(react_1.Component));
exports.default = GroupTagDistributionMeter;
//# sourceMappingURL=tagDistributionMeter.jsx.map