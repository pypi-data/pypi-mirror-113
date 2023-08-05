Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var requestLog_1 = tslib_1.__importDefault(require("./requestLog"));
var SentryApplicationDashboard = /** @class */ (function (_super) {
    tslib_1.__extends(SentryApplicationDashboard, _super);
    function SentryApplicationDashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SentryApplicationDashboard.prototype.getEndpoints = function () {
        var appSlug = this.props.params.appSlug;
        // Default time range for now: 90 days ago to now
        var now = Math.floor(new Date().getTime() / 1000);
        var ninety_days_ago = 3600 * 24 * 90;
        return [
            [
                'stats',
                "/sentry-apps/" + appSlug + "/stats/",
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            [
                'interactions',
                "/sentry-apps/" + appSlug + "/interaction/",
                { query: { since: now - ninety_days_ago, until: now } },
            ],
            ['app', "/sentry-apps/" + appSlug + "/"],
        ];
    };
    SentryApplicationDashboard.prototype.getTitle = function () {
        return locale_1.t('Integration Dashboard');
    };
    SentryApplicationDashboard.prototype.renderInstallData = function () {
        var _a = this.state, app = _a.app, stats = _a.stats;
        var totalUninstalls = stats.totalUninstalls, totalInstalls = stats.totalInstalls;
        return (<react_1.Fragment>
        <h5>{locale_1.t('Installation & Interaction Data')}</h5>
        <Row>
          {app.datePublished ? (<StatsSection>
              <StatsHeader>{locale_1.t('Date published')}</StatsHeader>
              <dateTime_1.default dateOnly date={app.datePublished}/>
            </StatsSection>) : null}
          <StatsSection>
            <StatsHeader>{locale_1.t('Total installs')}</StatsHeader>
            <p>{totalInstalls}</p>
          </StatsSection>
          <StatsSection>
            <StatsHeader>{locale_1.t('Total uninstalls')}</StatsHeader>
            <p>{totalUninstalls}</p>
          </StatsSection>
        </Row>
        {this.renderInstallCharts()}
      </react_1.Fragment>);
    };
    SentryApplicationDashboard.prototype.renderInstallCharts = function () {
        var _a = this.state.stats, installStats = _a.installStats, uninstallStats = _a.uninstallStats;
        var installSeries = {
            data: installStats.map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
            seriesName: locale_1.t('installed'),
        };
        var uninstallSeries = {
            data: uninstallStats.map(function (point) { return ({
                name: point[0] * 1000,
                value: point[1],
            }); }),
            seriesName: locale_1.t('uninstalled'),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Installations/Uninstallations over Last 90 Days')}</panels_1.PanelHeader>
        <ChartWrapper>
          <barChart_1.default series={[installSeries, uninstallSeries]} height={150} stacked isGroupedByDate legend={{
                show: true,
                orient: 'horizontal',
                data: ['installed', 'uninstalled'],
                itemWidth: 15,
            }} yAxis={{ type: 'value', minInterval: 1, max: 'dataMax' }} xAxis={{ type: 'time' }} grid={{ left: space_1.default(4), right: space_1.default(4) }}/>
        </ChartWrapper>
      </panels_1.Panel>);
    };
    SentryApplicationDashboard.prototype.renderIntegrationViews = function () {
        var views = this.state.interactions.views;
        var _a = this.props.params, appSlug = _a.appSlug, orgId = _a.orgId;
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Integration Views')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <InteractionsChart data={{ Views: views }}/>
        </panels_1.PanelBody>

        <panels_1.PanelFooter>
          <StyledFooter>
            {locale_1.t('Integration views are measured through views on the ')}
            <link_1.default to={"/sentry-apps/" + appSlug + "/external-install/"}>
              {locale_1.t('external installation page')}
            </link_1.default>
            {locale_1.t(' and views on the Learn More/Install modal on the ')}
            <link_1.default to={"/settings/" + orgId + "/integrations/"}>{locale_1.t('integrations page')}</link_1.default>
          </StyledFooter>
        </panels_1.PanelFooter>
      </panels_1.Panel>);
    };
    SentryApplicationDashboard.prototype.renderComponentInteractions = function () {
        var componentInteractions = this.state.interactions.componentInteractions;
        var componentInteractionsDetails = {
            'stacktrace-link': locale_1.t('Each link click or context menu open counts as one interaction'),
            'issue-link': locale_1.t('Each open of the issue link modal counts as one interaction'),
        };
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Component Interactions')}</panels_1.PanelHeader>

        <panels_1.PanelBody>
          <InteractionsChart data={componentInteractions}/>
        </panels_1.PanelBody>

        <panels_1.PanelFooter>
          <StyledFooter>
            {Object.keys(componentInteractions).map(function (component, idx) {
                return componentInteractionsDetails[component] && (<react_1.Fragment key={idx}>
                    <strong>{component + ": "}</strong>
                    {componentInteractionsDetails[component]}
                    <br />
                  </react_1.Fragment>);
            })}
          </StyledFooter>
        </panels_1.PanelFooter>
      </panels_1.Panel>);
    };
    SentryApplicationDashboard.prototype.renderBody = function () {
        var app = this.state.app;
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Integration Dashboard') + " - " + app.name}/>
        {app.status === 'published' && this.renderInstallData()}
        {app.status === 'published' && this.renderIntegrationViews()}
        {app.schema.elements && this.renderComponentInteractions()}
        <requestLog_1.default app={app}/>
      </div>);
    };
    return SentryApplicationDashboard;
}(asyncView_1.default));
exports.default = SentryApplicationDashboard;
var InteractionsChart = function (_a) {
    var data = _a.data;
    var elementInteractionsSeries = Object.keys(data).map(function (key) {
        var seriesData = data[key].map(function (point) { return ({
            value: point[1],
            name: point[0] * 1000,
        }); });
        return {
            seriesName: key,
            data: seriesData,
        };
    });
    return (<ChartWrapper>
      <lineChart_1.default isGroupedByDate series={elementInteractionsSeries} grid={{ left: space_1.default(4), right: space_1.default(4) }} legend={{
            show: true,
            orient: 'horizontal',
            data: Object.keys(data),
        }}/>
    </ChartWrapper>);
};
var Row = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StatsSection = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(4));
var StatsHeader = styled_1.default('h6')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: 12px;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  margin-bottom: ", ";\n  font-size: 12px;\n  text-transform: uppercase;\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.subText; });
var StyledFooter = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(1.5));
var ChartWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space_1.default(3));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map