Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledPanel = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var eventsChart_1 = tslib_1.__importDefault(require("app/components/charts/eventsChart"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var dates_1 = require("app/utils/dates");
var types_1 = require("app/utils/discover/types");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var chartFooter_1 = tslib_1.__importDefault(require("./chartFooter"));
var ResultsChart = /** @class */ (function (_super) {
    tslib_1.__extends(ResultsChart, _super);
    function ResultsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResultsChart.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, eventView = _a.eventView, restProps = tslib_1.__rest(_a, ["eventView"]);
        var nextEventView = nextProps.eventView, restNextProps = tslib_1.__rest(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView)) {
            return true;
        }
        return !isEqual_1.default(restProps, restNextProps);
    };
    ResultsChart.prototype.render = function () {
        var _a = this.props, api = _a.api, eventView = _a.eventView, location = _a.location, organization = _a.organization, router = _a.router, confirmedQuery = _a.confirmedQuery;
        var yAxisValue = eventView.getYAxis();
        var globalSelection = eventView.getGlobalSelection();
        var start = globalSelection.datetime.start
            ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.start)
            : null;
        var end = globalSelection.datetime.end
            ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.end)
            : null;
        var utc = getParams_1.getParams(location.query).utc;
        var apiPayload = eventView.getEventsAPIPayload(location);
        var display = eventView.getDisplayMode();
        var isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
        var isPeriod = display === types_1.DisplayModes.DEFAULT || display === types_1.DisplayModes.TOP5;
        var isDaily = display === types_1.DisplayModes.DAILYTOP5 || display === types_1.DisplayModes.DAILY;
        var isPrevious = display === types_1.DisplayModes.PREVIOUS;
        return (<react_1.Fragment>
        {getDynamicText_1.default({
                value: (<eventsChart_1.default api={api} router={router} query={apiPayload.query} organization={organization} showLegend yAxis={yAxisValue} projects={globalSelection.projects} environments={globalSelection.environments} start={start} end={end} period={globalSelection.datetime.period} disablePrevious={!isPrevious} disableReleases={!isPeriod} field={isTopEvents ? apiPayload.field : undefined} interval={eventView.interval} showDaily={isDaily} topEvents={isTopEvents ? types_1.TOP_N : undefined} orderby={isTopEvents ? queryString_1.decodeScalar(apiPayload.sort) : undefined} utc={utc === 'true'} confirmedQuery={confirmedQuery}/>),
                fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
            })}
      </react_1.Fragment>);
    };
    return ResultsChart;
}(react_1.Component));
var ResultsChartContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ResultsChartContainer, _super);
    function ResultsChartContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResultsChartContainer.prototype.shouldComponentUpdate = function (nextProps) {
        var _a = this.props, eventView = _a.eventView, restProps = tslib_1.__rest(_a, ["eventView"]);
        var nextEventView = nextProps.eventView, restNextProps = tslib_1.__rest(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView) ||
            this.props.confirmedQuery !== nextProps.confirmedQuery) {
            return true;
        }
        return !isEqual_1.default(restProps, restNextProps);
    };
    ResultsChartContainer.prototype.render = function () {
        var _a = this.props, api = _a.api, eventView = _a.eventView, location = _a.location, router = _a.router, total = _a.total, onAxisChange = _a.onAxisChange, onDisplayChange = _a.onDisplayChange, organization = _a.organization, confirmedQuery = _a.confirmedQuery;
        var yAxisValue = eventView.getYAxis();
        var hasQueryFeature = organization.features.includes('discover-query');
        var displayOptions = eventView.getDisplayOptions().filter(function (opt) {
            // top5 modes are only available with larger packages in saas.
            // We remove instead of disable here as showing tooltips in dropdown
            // menus is clunky.
            if ([types_1.DisplayModes.TOP5, types_1.DisplayModes.DAILYTOP5].includes(opt.value) &&
                !hasQueryFeature) {
                return false;
            }
            return true;
        });
        return (<exports.StyledPanel>
        <ResultsChart api={api} eventView={eventView} location={location} organization={organization} router={router} confirmedQuery={confirmedQuery}/>
        <chartFooter_1.default total={total} yAxisValue={yAxisValue} yAxisOptions={eventView.getYAxisOptions()} onAxisChange={onAxisChange} displayOptions={displayOptions} displayMode={eventView.getDisplayMode()} onDisplayChange={onDisplayChange}/>
      </exports.StyledPanel>);
    };
    return ResultsChartContainer;
}(react_1.Component));
exports.default = withApi_1.default(ResultsChartContainer);
exports.StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1;
//# sourceMappingURL=resultsChart.jsx.map