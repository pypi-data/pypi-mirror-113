Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var loadingPanel_1 = tslib_1.__importDefault(require("app/components/charts/loadingPanel"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var dates_1 = require("app/utils/dates");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var data_1 = require("../data");
var styles_2 = require("../styles");
var chart_1 = tslib_1.__importDefault(require("./chart"));
var footer_1 = tslib_1.__importDefault(require("./footer"));
var Container = /** @class */ (function (_super) {
    tslib_1.__extends(Container, _super);
    function Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Container.prototype.getChartParameters = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var options = data_1.getAxisOptions(organization);
        var left = options.find(function (opt) { return opt.value === location.query.left; }) || options[0];
        var right = options.find(function (opt) { return opt.value === location.query.right; }) || options[1];
        return [left, right];
    };
    Container.prototype.render = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, eventView = _a.eventView, router = _a.router;
        // construct request parameters for fetching chart data
        var globalSelection = eventView.getGlobalSelection();
        var start = globalSelection.datetime.start
            ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.start)
            : null;
        var end = globalSelection.datetime.end
            ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.end)
            : null;
        var utc = getParams_1.getParams(location.query).utc;
        var axisOptions = this.getChartParameters();
        var apiPayload = eventView.getEventsAPIPayload(location);
        return (<panels_1.Panel>
        <eventsRequest_1.default organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={utils_1.getInterval({
                start: start,
                end: end,
                period: globalSelection.datetime.period,
            }, true)} showLoading={false} query={apiPayload.query} includePrevious={false} yAxis={axisOptions.map(function (opt) { return opt.value; })} partial>
          {function (_a) {
                var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, results = _a.results;
                if (errored) {
                    return (<styles_2.ErrorPanel>
                  <icons_1.IconWarning color="gray300" size="lg"/>
                </styles_2.ErrorPanel>);
                }
                return (<react_1.Fragment>
                <styles_2.DoubleHeaderContainer>
                  {axisOptions.map(function (option, i) { return (<div key={option.label + ":" + i}>
                      <styles_1.HeaderTitle>
                        {option.label}
                        <questionTooltip_1.default position="top" size="sm" title={option.tooltip}/>
                      </styles_1.HeaderTitle>
                    </div>); })}
                </styles_2.DoubleHeaderContainer>
                {results ? (getDynamicText_1.default({
                        value: (<chart_1.default data={results} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} start={start} end={end} utc={utc === 'true'}/>),
                        fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                    })) : (<loadingPanel_1.default data-test-id="events-request-loading"/>)}
              </react_1.Fragment>);
            }}
        </eventsRequest_1.default>
        <footer_1.default api={api} leftAxis={axisOptions[0].value} rightAxis={axisOptions[1].value} organization={organization} eventView={eventView} location={location}/>
      </panels_1.Panel>);
    };
    return Container;
}(react_1.Component));
exports.default = withApi_1.default(Container);
//# sourceMappingURL=index.jsx.map