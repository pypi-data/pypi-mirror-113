Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var globalAppStoreConnectUpdateAlert_1 = tslib_1.__importDefault(require("app/components/globalAppStoreConnectUpdateAlert"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var navigationButtonGroup_1 = tslib_1.__importDefault(require("app/components/navigationButtonGroup"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var quickTrace_1 = tslib_1.__importDefault(require("./quickTrace"));
var formatDateDelta = function (reference, observed) {
    var duration = moment_timezone_1.default.duration(Math.abs(+observed - +reference));
    var hours = Math.floor(+duration / (60 * 60 * 1000));
    var minutes = duration.minutes();
    var results = [];
    if (hours) {
        results.push(hours + " hour" + (hours !== 1 ? 's' : ''));
    }
    if (minutes) {
        results.push(minutes + " minute" + (minutes !== 1 ? 's' : ''));
    }
    if (results.length === 0) {
        results.push('a few seconds');
    }
    return results.join(', ');
};
var GroupEventToolbar = /** @class */ (function (_super) {
    tslib_1.__extends(GroupEventToolbar, _super);
    function GroupEventToolbar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupEventToolbar.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event.id !== nextProps.event.id;
    };
    GroupEventToolbar.prototype.handleTraceLink = function (organization) {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'quick_trace.trace_id.clicked',
            eventName: 'Quick Trace: Trace ID clicked',
            organization_id: parseInt(organization.id, 10),
            source: 'issues',
        });
    };
    GroupEventToolbar.prototype.getDateTooltip = function () {
        var _a;
        var evt = this.props.event;
        var user = configStore_1.default.get('user');
        var options = (_a = user === null || user === void 0 ? void 0 : user.options) !== null && _a !== void 0 ? _a : {};
        var format = options.clock24Hours ? 'HH:mm:ss z' : 'LTS z';
        var dateCreated = moment_timezone_1.default(evt.dateCreated);
        var dateReceived = evt.dateReceived ? moment_timezone_1.default(evt.dateReceived) : null;
        return (<DescriptionList className="flat">
        <dt>Occurred</dt>
        <dd>
          {dateCreated.format('ll')}
          <br />
          {dateCreated.format(format)}
        </dd>
        {dateReceived && (<react_1.Fragment>
            <dt>Received</dt>
            <dd>
              {dateReceived.format('ll')}
              <br />
              {dateReceived.format(format)}
            </dd>
            <dt>Latency</dt>
            <dd>{formatDateDelta(dateCreated, dateReceived)}</dd>
          </react_1.Fragment>)}
      </DescriptionList>);
    };
    GroupEventToolbar.prototype.render = function () {
        var evt = this.props.event;
        var _a = this.props, group = _a.group, organization = _a.organization, location = _a.location, project = _a.project;
        var groupId = group.id;
        var baseEventsPath = "/organizations/" + organization.slug + "/issues/" + groupId + "/events/";
        // TODO: possible to define this as a route in react-router, but without a corresponding
        //       React component?
        var jsonUrl = "/organizations/" + organization.slug + "/issues/" + groupId + "/events/" + evt.id + "/json/";
        var latencyThreshold = 30 * 60 * 1000; // 30 minutes
        var isOverLatencyThreshold = evt.dateReceived &&
            Math.abs(+moment_timezone_1.default(evt.dateReceived) - +moment_timezone_1.default(evt.dateCreated)) > latencyThreshold;
        return (<Wrapper>
        <StyledNavigationButtonGroup hasPrevious={!!evt.previousEventID} hasNext={!!evt.nextEventID} links={[
                { pathname: baseEventsPath + "oldest/", query: location.query },
                { pathname: "" + baseEventsPath + evt.previousEventID + "/", query: location.query },
                { pathname: "" + baseEventsPath + evt.nextEventID + "/", query: location.query },
                { pathname: baseEventsPath + "latest/", query: location.query },
            ]} size="small"/>
        <Heading>
          {locale_1.t('Event')}{' '}
          <EventIdLink to={"" + baseEventsPath + evt.id + "/"}>{evt.eventID}</EventIdLink>
          <LinkContainer>
            <externalLink_1.default href={jsonUrl}>
              {'JSON'} (<fileSize_1.default bytes={evt.size}/>)
            </externalLink_1.default>
          </LinkContainer>
        </Heading>
        <tooltip_1.default title={this.getDateTooltip()} disableForVisualTest>
          <StyledDateTime date={getDynamicText_1.default({ value: evt.dateCreated, fixed: 'Dummy timestamp' })}/>
          {isOverLatencyThreshold && <StyledIconWarning color="yellow300"/>}
        </tooltip_1.default>
        <StyledGlobalAppStoreConnectUpdateAlert project={project} organization={organization} isCompact/>
        <quickTrace_1.default event={evt} group={group} organization={organization} location={location}/>
      </Wrapper>);
    };
    return GroupEventToolbar;
}(react_1.Component));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  margin-bottom: -5px;\n  /* z-index seems unnecessary, but increasing (instead of removing) just in case(billy) */\n  /* Fixes tooltips in toolbar having lower z-index than .btn-group .btn.active */\n  z-index: 3;\n  padding: 20px 30px 20px 40px;\n\n  @media (max-width: 767px) {\n    display: none;\n  }\n"], ["\n  position: relative;\n  margin-bottom: -5px;\n  /* z-index seems unnecessary, but increasing (instead of removing) just in case(billy) */\n  /* Fixes tooltips in toolbar having lower z-index than .btn-group .btn.active */\n  z-index: 3;\n  padding: 20px 30px 20px 40px;\n\n  @media (max-width: 767px) {\n    display: none;\n  }\n"])));
var EventIdLink = styled_1.default(react_router_1.Link)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n"], ["\n  font-weight: normal;\n"])));
var Heading = styled_1.default('h4')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  line-height: 1.3;\n  margin: 0;\n  font-size: ", ";\n"], ["\n  line-height: 1.3;\n  margin: 0;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledNavigationButtonGroup = styled_1.default(navigationButtonGroup_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  float: right;\n"], ["\n  float: right;\n"])));
var StyledIconWarning = styled_1.default(icons_1.IconWarning)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  position: relative;\n  top: ", ";\n"], ["\n  margin-left: ", ";\n  position: relative;\n  top: ", ";\n"])), space_1.default(0.5), space_1.default(0.25));
var StyledDateTime = styled_1.default(dateTime_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  border-bottom: 1px dotted #dfe3ea;\n  color: ", ";\n"], ["\n  border-bottom: 1px dotted #dfe3ea;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledGlobalAppStoreConnectUpdateAlert = styled_1.default(globalAppStoreConnectUpdateAlert_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(0.5), space_1.default(1));
var LinkContainer = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n  font-weight: normal;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n  font-weight: normal;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"])), space_1.default(1), space_1.default(1), function (p) { return p.theme.border; });
var DescriptionList = styled_1.default('dl')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  margin: 0;\n  min-width: 200px;\n  max-width: 250px;\n"], ["\n  text-align: left;\n  margin: 0;\n  min-width: 200px;\n  max-width: 250px;\n"])));
exports.default = GroupEventToolbar;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=eventToolbar.jsx.map