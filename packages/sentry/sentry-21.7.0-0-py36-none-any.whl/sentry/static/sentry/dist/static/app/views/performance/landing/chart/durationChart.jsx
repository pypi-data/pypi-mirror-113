Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var withRouter_1 = tslib_1.__importDefault(require("react-router/lib/withRouter"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var styles_1 = require("app/components/charts/styles");
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var chart_1 = tslib_1.__importDefault(require("../../charts/chart"));
var styles_2 = require("../../styles");
var utils_2 = require("../display/utils");
function DurationChart(props) {
    var organization = props.organization, api = props.api, eventView = props.eventView, location = props.location, router = props.router, field = props.field, title = props.title, titleTooltip = props.titleTooltip, backupField = props.backupField, usingBackupAxis = props.usingBackupAxis;
    // construct request parameters for fetching chart data
    var globalSelection = eventView.getGlobalSelection();
    var start = globalSelection.datetime.start
        ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.start)
        : null;
    var end = globalSelection.datetime.end
        ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.end)
        : null;
    var utc = getParams_1.getParams(location.query).utc;
    var _backupField = backupField ? [backupField] : [];
    var apiPayload = eventView.getEventsAPIPayload(location);
    return (<eventsRequest_1.default organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={utils_1.getInterval({
            start: start,
            end: end,
            period: globalSelection.datetime.period,
        }, true)} showLoading={false} query={apiPayload.query} includePrevious={false} yAxis={tslib_1.__spreadArray([field], tslib_1.__read(_backupField))} partial hideError>
      {function (_a) {
            var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, singleAxisResults = _a.timeseriesData, multiAxisResults = _a.results;
            var _field = usingBackupAxis ? utils_2.getFieldOrBackup(field, backupField) : field;
            var results = singleAxisResults
                ? singleAxisResults
                : [multiAxisResults === null || multiAxisResults === void 0 ? void 0 : multiAxisResults.find(function (r) { return r.seriesName === _field; })].filter(Boolean);
            var series = results
                ? results.map(function (_a) {
                    var rest = tslib_1.__rest(_a, []);
                    return tslib_1.__assign(tslib_1.__assign({}, rest), { seriesName: _field });
                })
                : [];
            if (errored) {
                return (<errorPanel_1.default>
              <icons_1.IconWarning color="gray300" size="lg"/>
            </errorPanel_1.default>);
            }
            return (<div>
            <styles_2.DoubleHeaderContainer>
              <styles_1.HeaderTitleLegend>
                {title}
                <questionTooltip_1.default position="top" size="sm" title={titleTooltip}/>
              </styles_1.HeaderTitleLegend>
            </styles_2.DoubleHeaderContainer>
            {results && (<ChartContainer>
                <MaskContainer>
                  <transparentLoadingMask_1.default visible={loading}/>
                  {getDynamicText_1.default({
                        value: (<chart_1.default height={250} data={series} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} start={start} end={end} utc={utc === 'true'} grid={{
                                left: space_1.default(3),
                                right: space_1.default(3),
                                top: space_1.default(3),
                                bottom: loading || reloading ? space_1.default(4) : space_1.default(1.5),
                            }} disableMultiAxis/>),
                        fixed: <placeholder_1.default height="250px" testId="skeleton-ui"/>,
                    })}
                </MaskContainer>
              </ChartContainer>)}
          </div>);
        }}
    </eventsRequest_1.default>);
}
var ChartContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space_1.default(1));
var MaskContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
exports.default = withRouter_1.default(withApi_1.default(DurationChart));
var templateObject_1, templateObject_2;
//# sourceMappingURL=durationChart.jsx.map