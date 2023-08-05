Object.defineProperty(exports, "__esModule", { value: true });
exports.DisplayModes = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var react_2 = require("@emotion/react");
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var loadingPanel_1 = tslib_1.__importDefault(require("app/components/charts/loadingPanel"));
var optionSelector_1 = tslib_1.__importDefault(require("app/components/charts/optionSelector"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var chartPalette_1 = tslib_1.__importDefault(require("app/constants/chartPalette"));
var notAvailableMessages_1 = tslib_1.__importDefault(require("app/constants/notAvailableMessages"));
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
var data_1 = require("../performance/data");
var projectBaseEventsChart_1 = tslib_1.__importDefault(require("./charts/projectBaseEventsChart"));
var projectBaseSessionsChart_1 = tslib_1.__importDefault(require("./charts/projectBaseSessionsChart"));
var projectErrorsBasicChart_1 = tslib_1.__importDefault(require("./charts/projectErrorsBasicChart"));
var DisplayModes;
(function (DisplayModes) {
    DisplayModes["APDEX"] = "apdex";
    DisplayModes["FAILURE_RATE"] = "failure_rate";
    DisplayModes["TPM"] = "tpm";
    DisplayModes["ERRORS"] = "errors";
    DisplayModes["TRANSACTIONS"] = "transactions";
    DisplayModes["STABILITY"] = "crash_free";
    DisplayModes["SESSIONS"] = "sessions";
})(DisplayModes = exports.DisplayModes || (exports.DisplayModes = {}));
var ProjectCharts = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectCharts, _super);
    function ProjectCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.handleDisplayModeChange = function (value) {
            var _a;
            var _b = _this.props, location = _b.location, chartId = _b.chartId, chartIndex = _b.chartIndex, organization = _b.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: "project_detail.change_chart" + (chartIndex + 1),
                eventName: "Project Detail: Change Chart #" + (chartIndex + 1),
                organization_id: parseInt(organization.id, 10),
                metric: value,
            });
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), (_a = {}, _a[chartId] = value, _a)),
            });
        };
        _this.handleTotalValuesChange = function (value) {
            if (value !== _this.state.totalValues) {
                _this.setState({ totalValues: value });
            }
        };
        return _this;
    }
    Object.defineProperty(ProjectCharts.prototype, "defaultDisplayModes", {
        get: function () {
            var _a = this.props, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions;
            if (!hasSessions && !hasTransactions) {
                return [DisplayModes.ERRORS];
            }
            if (hasSessions && !hasTransactions) {
                return [DisplayModes.STABILITY, DisplayModes.ERRORS];
            }
            if (!hasSessions && hasTransactions) {
                return [DisplayModes.FAILURE_RATE, DisplayModes.APDEX];
            }
            return [DisplayModes.STABILITY, DisplayModes.APDEX];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "otherActiveDisplayModes", {
        get: function () {
            var _this = this;
            var _a = this.props, location = _a.location, visibleCharts = _a.visibleCharts, chartId = _a.chartId;
            return visibleCharts
                .filter(function (visibleChartId) { return visibleChartId !== chartId; })
                .map(function (urlKey) {
                return queryString_1.decodeScalar(location.query[urlKey], _this.defaultDisplayModes[visibleCharts.findIndex(function (value) { return value === urlKey; })]);
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayMode", {
        get: function () {
            var _a = this.props, location = _a.location, chartId = _a.chartId, chartIndex = _a.chartIndex;
            var displayMode = queryString_1.decodeScalar(location.query[chartId]) || this.defaultDisplayModes[chartIndex];
            if (!Object.values(DisplayModes).includes(displayMode)) {
                return this.defaultDisplayModes[chartIndex];
            }
            return displayMode;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayModes", {
        get: function () {
            var _a = this.props, organization = _a.organization, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions;
            var hasPerformance = organization.features.includes('performance-view');
            var noPerformanceTooltip = notAvailableMessages_1.default.performance;
            var noHealthTooltip = notAvailableMessages_1.default.releaseHealth;
            return [
                {
                    value: DisplayModes.STABILITY,
                    label: locale_1.t('Crash Free Sessions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.STABILITY) || !hasSessions,
                    tooltip: !hasSessions ? noHealthTooltip : undefined,
                },
                {
                    value: DisplayModes.APDEX,
                    label: locale_1.t('Apdex'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.APDEX) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.APDEX)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.FAILURE_RATE,
                    label: locale_1.t('Failure Rate'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.FAILURE_RATE) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.TPM,
                    label: locale_1.t('Transactions Per Minute'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TPM) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.TPM)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.ERRORS,
                    label: locale_1.t('Number of Errors'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.ERRORS),
                },
                {
                    value: DisplayModes.SESSIONS,
                    label: locale_1.t('Number of Sessions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.SESSIONS) || !hasSessions,
                    tooltip: !hasSessions ? noHealthTooltip : undefined,
                },
                {
                    value: DisplayModes.TRANSACTIONS,
                    label: locale_1.t('Number of Transactions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TRANSACTIONS) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions ? undefined : noPerformanceTooltip,
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "summaryHeading", {
        get: function () {
            switch (this.displayMode) {
                case DisplayModes.ERRORS:
                    return locale_1.t('Total Errors');
                case DisplayModes.STABILITY:
                case DisplayModes.SESSIONS:
                    return locale_1.t('Total Sessions');
                case DisplayModes.APDEX:
                case DisplayModes.FAILURE_RATE:
                case DisplayModes.TPM:
                case DisplayModes.TRANSACTIONS:
                default:
                    return locale_1.t('Total Transactions');
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "barChartInterval", {
        get: function () {
            var query = this.props.location.query;
            var diffInMinutes = utils_1.getDiffInMinutes(tslib_1.__assign(tslib_1.__assign({}, query), { period: queryString_1.decodeScalar(query.statsPeriod) }));
            if (diffInMinutes >= utils_1.TWO_WEEKS) {
                return '1d';
            }
            if (diffInMinutes >= utils_1.ONE_WEEK) {
                return '12h';
            }
            if (diffInMinutes > utils_1.TWENTY_FOUR_HOURS) {
                return '6h';
            }
            if (diffInMinutes === utils_1.TWENTY_FOUR_HOURS) {
                return '1h';
            }
            if (diffInMinutes <= utils_1.ONE_HOUR) {
                return '1m';
            }
            return '15m';
        },
        enumerable: false,
        configurable: true
    });
    ProjectCharts.prototype.render = function () {
        var _a = this.props, api = _a.api, router = _a.router, location = _a.location, organization = _a.organization, theme = _a.theme, projectId = _a.projectId, hasSessions = _a.hasSessions, query = _a.query;
        var totalValues = this.state.totalValues;
        var hasDiscover = organization.features.includes('discover-basic');
        var displayMode = this.displayMode;
        var apdexYAxis;
        var apdexPerformanceTerm;
        if (organization.features.includes('project-transaction-threshold')) {
            apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX_NEW;
            apdexYAxis = 'apdex()';
        }
        else {
            apdexPerformanceTerm = data_1.PERFORMANCE_TERM.APDEX;
            apdexYAxis = "apdex(" + organization.apdexThreshold + ")";
        }
        return (<panels_1.Panel>
        <styles_1.ChartContainer>
          {!utils_2.defined(hasSessions) ? (<loadingPanel_1.default />) : (<react_1.Fragment>
              {displayMode === DisplayModes.APDEX && (<projectBaseEventsChart_1.default title={locale_1.t('Apdex')} help={data_1.getTermHelp(organization, apdexPerformanceTerm)} query={new tokenizeSearch_1.QueryResults([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis={apdexYAxis} field={[apdexYAxis]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[chartPalette_1.default[0][0], theme.purple200]}/>)}
              {displayMode === DisplayModes.FAILURE_RATE && (<projectBaseEventsChart_1.default title={locale_1.t('Failure Rate')} help={data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE)} query={new tokenizeSearch_1.QueryResults([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="failure_rate()" field={["failure_rate()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.red300, theme.purple200]}/>)}
              {displayMode === DisplayModes.TPM && (<projectBaseEventsChart_1.default title={locale_1.t('Transactions Per Minute')} help={data_1.getTermHelp(organization, data_1.PERFORMANCE_TERM.TPM)} query={new tokenizeSearch_1.QueryResults([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="tpm()" field={["tpm()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.yellow300, theme.purple200]} disablePrevious/>)}
              {displayMode === DisplayModes.ERRORS &&
                    (hasDiscover ? (<projectBaseEventsChart_1.default title={locale_1.t('Number of Errors')} query={new tokenizeSearch_1.QueryResults([
                            '!event.type:transaction',
                            query !== null && query !== void 0 ? query : '',
                        ]).formatString()} yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.purple300, theme.purple200]} interval={this.barChartInterval} chartComponent={barChart_1.default} disableReleases/>) : (<projectErrorsBasicChart_1.default organization={organization} projectId={projectId} location={location} onTotalValuesChange={this.handleTotalValuesChange}/>))}
              {displayMode === DisplayModes.TRANSACTIONS && (<projectBaseEventsChart_1.default title={locale_1.t('Number of Transactions')} query={new tokenizeSearch_1.QueryResults([
                        'event.type:transaction',
                        query !== null && query !== void 0 ? query : '',
                    ]).formatString()} yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.gray200, theme.purple200]} interval={this.barChartInterval} chartComponent={barChart_1.default} disableReleases/>)}
              {displayMode === DisplayModes.STABILITY && (<projectBaseSessionsChart_1.default title={locale_1.t('Crash Free Sessions')} help={sessionTerm_1.getSessionTermDescription(sessionTerm_1.SessionTerm.STABILITY, null)} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode} query={query}/>)}
              {displayMode === DisplayModes.SESSIONS && (<projectBaseSessionsChart_1.default title={locale_1.t('Number of Sessions')} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode} disablePrevious query={query}/>)}
            </react_1.Fragment>)}
        </styles_1.ChartContainer>
        <styles_1.ChartControls>
          {/* if hasSessions is not yet defined, it means that request is still in progress and we can't decide what default chart to show */}
          {utils_2.defined(hasSessions) ? (<react_1.Fragment>
              <styles_1.InlineContainer>
                <styles_1.SectionHeading>{this.summaryHeading}</styles_1.SectionHeading>
                <styles_1.SectionValue>
                  {typeof totalValues === 'number'
                    ? totalValues.toLocaleString()
                    : '\u2014'}
                </styles_1.SectionValue>
              </styles_1.InlineContainer>
              <styles_1.InlineContainer>
                <optionSelector_1.default title={locale_1.t('Display')} selected={displayMode} options={this.displayModes} onChange={this.handleDisplayModeChange}/>
              </styles_1.InlineContainer>
            </react_1.Fragment>) : (<placeholder_1.default height="34px"/>)}
        </styles_1.ChartControls>
      </panels_1.Panel>);
    };
    return ProjectCharts;
}(react_1.Component));
exports.default = withApi_1.default(react_2.withTheme(ProjectCharts));
//# sourceMappingURL=projectCharts.jsx.map