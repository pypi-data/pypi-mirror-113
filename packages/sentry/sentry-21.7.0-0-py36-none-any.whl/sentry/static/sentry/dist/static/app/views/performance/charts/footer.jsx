Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var events_1 = require("app/actionCreators/events");
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var data_1 = require("../data");
var ChartFooter = /** @class */ (function (_super) {
    tslib_1.__extends(ChartFooter, _super);
    function ChartFooter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getEventsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !eventView_1.isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.mounted = false;
        return _this;
    }
    ChartFooter.prototype.componentDidMount = function () {
        this.mounted = true;
        this.fetchTotalCount();
    };
    ChartFooter.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugHasChanged = this.props.organization.slug !== prevProps.organization.slug;
        var shouldRefetch = this.shouldRefetchData(prevProps);
        if ((orgSlugHasChanged || shouldRefetch) && this.props.eventView.isValid()) {
            this.fetchTotalCount();
        }
    };
    ChartFooter.prototype.componentWillUnmount = function () {
        this.mounted = false;
    };
    ChartFooter.prototype.handleSelectorChange = function (key, value) {
        var _a;
        var _b = this.props, location = _b.location, organization = _b.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.overview.change_chart',
            eventName: 'Performance Views: Change Overview Chart',
            organization_id: parseInt(organization.id, 10),
            metric: value,
        });
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), (_a = {}, _a[key] = value, _a)),
        });
    };
    ChartFooter.prototype.fetchTotalCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, eventView, totals, err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView;
                        if (!eventView.isValid() || !this.mounted) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, events_1.fetchTotalCount(api, organization.slug, eventView.getEventsAPIPayload(location))];
                    case 2:
                        totals = _b.sent();
                        if (this.mounted) {
                            this.setState({ totalValues: totals });
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ChartFooter.prototype.render = function () {
        var _this = this;
        var _a = this.props, leftAxis = _a.leftAxis, organization = _a.organization, rightAxis = _a.rightAxis;
        var totalValues = this.state.totalValues;
        var value = typeof totalValues === 'number' ? totalValues.toLocaleString() : '-';
        var options = this.props.options || data_1.getAxisOptions(organization);
        var leftOptions = options.map(function (opt) { return (tslib_1.__assign(tslib_1.__assign({}, opt), { disabled: opt.value === rightAxis })); });
        var rightOptions = options.map(function (opt) { return (tslib_1.__assign(tslib_1.__assign({}, opt), { disabled: opt.value === leftAxis })); });
        return (<styles_1.ChartControls>
        <styles_1.InlineContainer>
          <styles_1.SectionHeading>{locale_1.t('Total Events')}</styles_1.SectionHeading>
          <styles_1.SectionValue>{value}</styles_1.SectionValue>
        </styles_1.InlineContainer>
        <styles_1.InlineContainer>
          <optionSelector_1.default title={locale_1.t('Display 1')} selected={leftAxis} options={leftOptions} onChange={function (val) { return _this.handleSelectorChange('left', val); }}/>
          <optionSelector_1.default title={locale_1.t('Display 2')} selected={rightAxis} options={rightOptions} onChange={function (val) { return _this.handleSelectorChange('right', val); }}/>
        </styles_1.InlineContainer>
      </styles_1.ChartControls>);
    };
    return ChartFooter;
}(react_1.Component));
exports.default = ChartFooter;
//# sourceMappingURL=footer.jsx.map