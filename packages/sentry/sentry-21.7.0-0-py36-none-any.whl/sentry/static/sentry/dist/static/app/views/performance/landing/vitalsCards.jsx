Object.defineProperty(exports, "__esModule", { value: true });
exports.VitalBar = exports.BackendCards = exports.FrontendCards = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var card_1 = tslib_1.__importDefault(require("app/components/card"));
var eventsRequest_1 = tslib_1.__importDefault(require("app/components/charts/eventsRequest"));
var styles_1 = require("app/components/charts/styles");
var utils_1 = require("app/components/charts/utils");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var sparklines_1 = tslib_1.__importDefault(require("app/components/sparklines"));
var line_1 = tslib_1.__importDefault(require("app/components/sparklines/line"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dates_1 = require("app/utils/dates");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var fields_1 = require("app/utils/discover/fields");
var constants_1 = require("app/utils/performance/vitals/constants");
var vitalsCardsDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
var queryString_1 = require("app/utils/queryString");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var colorBar_1 = tslib_1.__importDefault(require("../vitalDetail/colorBar"));
var utils_2 = require("../vitalDetail/utils");
var vitalPercents_1 = tslib_1.__importDefault(require("../vitalDetail/vitalPercents"));
var utils_3 = require("./utils");
function FrontendCards(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, _a = props.frontendOnly, frontendOnly = _a === void 0 ? false : _a;
    if (frontendOnly) {
        var defaultDisplay = utils_3.getDefaultDisplayFieldForPlatform(projects, eventView);
        var isFrontend = defaultDisplay === utils_3.LandingDisplayField.FRONTEND_PAGELOAD;
        if (!isFrontend) {
            return null;
        }
    }
    var vitals = [fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS];
    return (<vitalsCardsDiscoverQuery_1.default eventView={eventView} location={location} orgSlug={organization.slug} vitals={vitals}>
      {function (_a) {
            var isLoading = _a.isLoading, vitalsData = _a.vitalsData;
            return (<VitalsContainer>
            {vitals.map(function (vital) {
                    var _a, _b, _c;
                    var target = utils_2.vitalDetailRouteWithQuery({
                        orgSlug: organization.slug,
                        query: eventView.generateQueryStringObject(),
                        vitalName: vital,
                        projectID: queryString_1.decodeList(location.query.project),
                    });
                    var value = isLoading
                        ? '\u2014'
                        : getP75((_a = vitalsData === null || vitalsData === void 0 ? void 0 : vitalsData[vital]) !== null && _a !== void 0 ? _a : null, vital);
                    var chart = (<VitalBarContainer>
                  <VitalBar isLoading={isLoading} vital={vital} data={vitalsData}/>
                </VitalBarContainer>);
                    return (<link_1.default key={vital} to={target} data-test-id={"vitals-linked-card-" + utils_2.vitalAbbreviations[vital]}>
                  <VitalCard title={(_b = utils_2.vitalMap[vital]) !== null && _b !== void 0 ? _b : ''} tooltip={(_c = constants_1.WEB_VITAL_DETAILS[vital].description) !== null && _c !== void 0 ? _c : ''} value={isLoading ? '\u2014' : value} chart={chart} minHeight={150}/>
                </link_1.default>);
                })}
          </VitalsContainer>);
        }}
    </vitalsCardsDiscoverQuery_1.default>);
}
exports.FrontendCards = FrontendCards;
var VitalBarContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(1.5));
function _BackendCards(props) {
    var api = props.api, baseEventView = props.eventView, location = props.location, organization = props.organization;
    var functionNames = [
        'p75',
        'tpm',
        'failure_rate',
        'apdex',
    ];
    var functions = functionNames.map(function (fn) { return utils_3.getBackendFunction(fn, organization); });
    var eventView = baseEventView.withColumns(functions);
    // construct request parameters for fetching chart data
    var globalSelection = eventView.getGlobalSelection();
    var start = globalSelection.datetime.start
        ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.start)
        : undefined;
    var end = globalSelection.datetime.end
        ? dates_1.getUtcToLocalDateObject(globalSelection.datetime.end)
        : undefined;
    var apiPayload = eventView.getEventsAPIPayload(location);
    return (<discoverQuery_1.default location={location} eventView={eventView} orgSlug={organization.slug} limit={1} referrer="api.performance.vitals-cards">
      {function (_a) {
            var isSummaryLoading = _a.isLoading, tableData = _a.tableData;
            return (<eventsRequest_1.default api={api} organization={organization} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={utils_1.getInterval({
                    start: start || null,
                    end: end || null,
                    period: globalSelection.datetime.period,
                })} query={apiPayload.query} includePrevious={false} yAxis={eventView.getFields()} partial>
          {function (_a) {
                    var results = _a.results;
                    var series = results === null || results === void 0 ? void 0 : results.reduce(function (allSeries, oneSeries) {
                        allSeries[oneSeries.seriesName] = oneSeries.data.map(function (item) { return item.value; });
                        return allSeries;
                    }, {});
                    var fields = eventView
                        .getFields()
                        .map(function (fn, i) { return [functionNames[i], fn, series === null || series === void 0 ? void 0 : series[fn]]; });
                    return (<VitalsContainer>
                {fields.map(function (_a) {
                            var _b, _c;
                            var _d = tslib_1.__read(_a, 3), name = _d[0], fn = _d[1], data = _d[2];
                            var _e = utils_3.backendCardDetails(organization)[name], title = _e.title, tooltip = _e.tooltip, formatter = _e.formatter;
                            var alias = fields_1.getAggregateAlias(fn);
                            var rawValue = (_c = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c[alias];
                            var value = isSummaryLoading || rawValue === undefined
                                ? '\u2014'
                                : formatter(rawValue);
                            var chart = <SparklineChart data={data}/>;
                            return (<VitalCard key={name} title={title} tooltip={tooltip} value={value} chart={chart} horizontal minHeight={96} isNotInteractive/>);
                        })}
              </VitalsContainer>);
                }}
        </eventsRequest_1.default>);
        }}
    </discoverQuery_1.default>);
}
exports.BackendCards = withApi_1.default(_BackendCards);
function SparklineChart(props) {
    var data = props.data;
    var width = 150;
    var height = 24;
    var lineColor = theme_1.default.charts.getColorPalette(1)[0];
    return (<SparklineContainer data-test-id="sparkline" width={width} height={height}>
      <sparklines_1.default data={data} width={width} height={height}>
        <line_1.default style={{ stroke: lineColor, fill: 'none', strokeWidth: 3 }}/>
      </sparklines_1.default>
    </SparklineContainer>);
}
var SparklineContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-grow: 4;\n  max-height: ", "px;\n  max-width: ", "px;\n  margin: ", " ", " ", " ", ";\n"], ["\n  flex-grow: 4;\n  max-height: ", "px;\n  max-width: ", "px;\n  margin: ", " ", " ", " ", ";\n"])), function (p) { return p.height; }, function (p) { return p.width; }, space_1.default(1), space_1.default(0), space_1.default(0.5), space_1.default(3));
var VitalsContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
function VitalBar(props) {
    var _a;
    var isLoading = props.isLoading, data = props.data, vital = props.vital, value = props.value, _b = props.showBar, showBar = _b === void 0 ? true : _b, _c = props.showStates, showStates = _c === void 0 ? false : _c, _d = props.showDurationDetail, showDurationDetail = _d === void 0 ? false : _d, _e = props.showVitalPercentNames, showVitalPercentNames = _e === void 0 ? false : _e;
    if (isLoading) {
        return showStates ? <placeholder_1.default height="48px"/> : null;
    }
    var emptyState = showStates ? (<EmptyVitalBar small>{locale_1.t('No vitals found')}</EmptyVitalBar>) : null;
    if (!data) {
        return emptyState;
    }
    var counts = {
        poor: 0,
        meh: 0,
        good: 0,
        total: 0,
    };
    var vitals = Array.isArray(vital) ? vital : [vital];
    vitals.forEach(function (vitalName) {
        var _a;
        var c = (_a = data === null || data === void 0 ? void 0 : data[vitalName]) !== null && _a !== void 0 ? _a : {};
        Object.keys(counts).forEach(function (countKey) { return (counts[countKey] += c[countKey]); });
    });
    if (!counts.total) {
        return emptyState;
    }
    var p75 = Array.isArray(vital)
        ? null
        : value !== null && value !== void 0 ? value : getP75((_a = data === null || data === void 0 ? void 0 : data[vital]) !== null && _a !== void 0 ? _a : null, vital);
    var percents = getPercentsFromCounts(counts);
    var colorStops = getColorStopsFromPercents(percents);
    return (<React.Fragment>
      {showBar && <colorBar_1.default colorStops={colorStops}/>}
      <BarDetail>
        {showDurationDetail && p75 && (<div data-test-id="vital-bar-p75">
            {locale_1.t('The p75 for all transactions is ')}
            <strong>{p75}</strong>
          </div>)}
        <vitalPercents_1.default vital={vital} percents={percents} showVitalPercentNames={showVitalPercentNames}/>
      </BarDetail>
    </React.Fragment>);
}
exports.VitalBar = VitalBar;
var EmptyVitalBar = styled_1.default(emptyStateWarning_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  height: 48px;\n  padding: ", " 15%;\n"], ["\n  height: 48px;\n  padding: ", " 15%;\n"])), space_1.default(1.5));
function VitalCard(props) {
    var chart = props.chart, minHeight = props.minHeight, horizontal = props.horizontal, title = props.title, tooltip = props.tooltip, value = props.value, isNotInteractive = props.isNotInteractive;
    return (<StyledCard interactive={!isNotInteractive} minHeight={minHeight}>
      <styles_1.HeaderTitle>
        <OverflowEllipsis>{locale_1.t(title)}</OverflowEllipsis>
        <questionTooltip_1.default size="sm" position="top" title={tooltip}/>
      </styles_1.HeaderTitle>
      <CardContent horizontal={horizontal}>
        <CardValue>{value}</CardValue>
        {chart}
      </CardContent>
    </StyledCard>);
}
var CardContent = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  flex-direction: ", ";\n  justify-content: space-between;\n"], ["\n  width: 100%;\n  display: flex;\n  flex-direction: ", ";\n  justify-content: space-between;\n"])), function (p) { return (p.horizontal ? 'row' : 'column'); });
var StyledCard = styled_1.default(card_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  margin-bottom: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(2), space_1.default(3), space_1.default(2), function (p) { return p.minHeight && "min-height: " + p.minHeight + "px"; });
function getP75(data, vitalName) {
    var _a;
    var p75 = (_a = data === null || data === void 0 ? void 0 : data.p75) !== null && _a !== void 0 ? _a : null;
    if (p75 === null) {
        return '\u2014';
    }
    else {
        return vitalName === fields_1.WebVital.CLS ? p75.toFixed(2) : p75.toFixed(0) + "ms";
    }
}
function getPercentsFromCounts(_a) {
    var poor = _a.poor, meh = _a.meh, good = _a.good, total = _a.total;
    var poorPercent = poor / total;
    var mehPercent = meh / total;
    var goodPercent = good / total;
    var percents = [
        {
            vitalState: utils_2.VitalState.GOOD,
            percent: goodPercent,
        },
        {
            vitalState: utils_2.VitalState.MEH,
            percent: mehPercent,
        },
        {
            vitalState: utils_2.VitalState.POOR,
            percent: poorPercent,
        },
    ];
    return percents;
}
function getColorStopsFromPercents(percents) {
    return percents.map(function (_a) {
        var percent = _a.percent, vitalState = _a.vitalState;
        return ({
            percent: percent,
            color: utils_2.vitalStateColors[vitalState],
        });
    });
}
var BarDetail = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"], ["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; });
var CardValue = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: 32px;\n  margin-top: ", ";\n"], ["\n  font-size: 32px;\n  margin-top: ", ";\n"])), space_1.default(1));
var OverflowEllipsis = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=vitalsCards.jsx.map