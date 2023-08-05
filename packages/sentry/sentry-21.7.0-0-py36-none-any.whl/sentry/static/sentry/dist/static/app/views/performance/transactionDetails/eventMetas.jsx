Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var utils_1 = require("app/utils/performance/quickTrace/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var quickTraceMeta_1 = tslib_1.__importDefault(require("./quickTraceMeta"));
var styles_1 = require("./styles");
/**
 * This should match the breakpoint chosen for the `EventDetailHeader` below
 */
var BREAKPOINT_MEDIA_QUERY = "(min-width: " + theme_1.default.breakpoints[2] + ")";
var EventMetas = /** @class */ (function (_super) {
    tslib_1.__extends(EventMetas, _super);
    function EventMetas() {
        var _a, _b, _c;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = {
            isLargeScreen: (_b = (_a = window.matchMedia) === null || _a === void 0 ? void 0 : _a.call(window, BREAKPOINT_MEDIA_QUERY)) === null || _b === void 0 ? void 0 : _b.matches,
        };
        _this.mq = (_c = window.matchMedia) === null || _c === void 0 ? void 0 : _c.call(window, BREAKPOINT_MEDIA_QUERY);
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                isLargeScreen: changed.matches,
            });
        };
        return _this;
    }
    EventMetas.prototype.componentDidMount = function () {
        if (this.mq) {
            this.mq.addListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.componentWillUnmount = function () {
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.render = function () {
        var _a = this.props, event = _a.event, organization = _a.organization, projectId = _a.projectId, location = _a.location, quickTrace = _a.quickTrace, meta = _a.meta, errorDest = _a.errorDest, transactionDest = _a.transactionDest;
        var isLargeScreen = this.state.isLargeScreen;
        var type = utils_1.isTransaction(event) ? 'transaction' : 'event';
        var timestamp = (<timeSince_1.default date={event.dateCreated || (event.endTimestamp || 0) * 1000}/>);
        var httpStatus = <HttpStatus event={event}/>;
        return (<projects_1.default orgId={organization.slug} slugs={[projectId]}>
        {function (_a) {
                var _b, _c, _d;
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === projectId; });
                return (<EventDetailHeader type={type}>
              <styles_1.MetaData headingText={locale_1.t('Event ID')} tooltipText={locale_1.t('The unique ID assigned to this %s.', type)} bodyText={<EventID event={event}/>} subtext={<projectBadge_1.default project={project ? project : { slug: projectId }} avatarSize={16}/>}/>
              {utils_1.isTransaction(event) ? (<styles_1.MetaData headingText={locale_1.t('Event Duration')} tooltipText={locale_1.t('The time elapsed between the start and end of this transaction.')} bodyText={formatters_1.getDuration(event.endTimestamp - event.startTimestamp, 2, true)} subtext={timestamp}/>) : (<styles_1.MetaData headingText={locale_1.t('Created')} tooltipText={locale_1.t('The time at which this event was created.')} bodyText={timestamp} subtext={getDynamicText_1.default({
                            value: <dateTime_1.default date={event.dateCreated}/>,
                            fixed: 'May 6, 2021 3:27:01 UTC',
                        })}/>)}
              {utils_1.isTransaction(event) && (<styles_1.MetaData headingText={locale_1.t('Status')} tooltipText={locale_1.t('The status of this transaction indicating if it succeeded or otherwise.')} bodyText={(_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.status) !== null && _d !== void 0 ? _d : '\u2014'} subtext={httpStatus}/>)}
              <QuickTraceContainer>
                <quickTraceMeta_1.default event={event} project={project} organization={organization} location={location} quickTrace={quickTrace} traceMeta={meta} anchor={isLargeScreen ? 'right' : 'left'} errorDest={errorDest} transactionDest={transactionDest}/>
              </QuickTraceContainer>
            </EventDetailHeader>);
            }}
      </projects_1.default>);
    };
    return EventMetas;
}(React.Component));
var EventDetailHeader = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ", ";\n    grid-row-gap: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ", ";\n    grid-row-gap: 0;\n  }\n"])), function (p) { return (p.type === 'transaction' ? 3 : 2); }, space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) {
    return p.type === 'transaction'
        ? 'grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;'
        : 'grid-template-columns: minmax(160px, 1fr) minmax(200px, 1fr) 6fr;';
});
var QuickTraceContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"], ["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
function EventID(_a) {
    var event = _a.event;
    return (<clipboard_1.default value={event.eventID}>
      <EventIDContainer>
        <EventIDWrapper>{events_1.getShortEventId(event.eventID)}</EventIDWrapper>
        <tooltip_1.default title={event.eventID} position="top">
          <icons_1.IconCopy color="subText"/>
        </tooltip_1.default>
      </EventIDContainer>
    </clipboard_1.default>);
}
var EventIDContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n"], ["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n"])));
var EventIDWrapper = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
function HttpStatus(_a) {
    var event = _a.event;
    var tags = event.tags;
    var emptyStatus = <React.Fragment>{'\u2014'}</React.Fragment>;
    if (!Array.isArray(tags)) {
        return emptyStatus;
    }
    var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
    if (!tag) {
        return emptyStatus;
    }
    return <React.Fragment>HTTP {tag.value}</React.Fragment>;
}
exports.default = EventMetas;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventMetas.jsx.map