Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var styles_1 = require("app/components/charts/styles");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var panels_1 = require("app/components/panels");
var seenByList_1 = tslib_1.__importDefault(require("app/components/seenByList"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var details_1 = require("app/views/alerts/details");
var statusItem_1 = require("app/views/alerts/details/activity/statusItem");
var types_1 = require("app/views/alerts/types");
var TimelineIncident = /** @class */ (function (_super) {
    tslib_1.__extends(TimelineIncident, _super);
    function TimelineIncident() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TimelineIncident.prototype.renderActivity = function (activity, idx) {
        var _a, _b;
        var _c = this.props, incident = _c.incident, rule = _c.rule;
        var activities = incident.activities;
        var last = activities && idx === activities.length - 1;
        var authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
        var isDetected = activity.type === types_1.IncidentActivityType.DETECTED;
        var isStarted = activity.type === types_1.IncidentActivityType.STARTED;
        var isClosed = activity.type === types_1.IncidentActivityType.STATUS_CHANGE &&
            activity.value === "" + types_1.IncidentStatus.CLOSED;
        var isTriggerChange = activity.type === types_1.IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if ((!isStarted && !isDetected && !isClosed && !isTriggerChange) ||
            !activities ||
            !activities.length) {
            return null;
        }
        var currentTrigger = statusItem_1.getTriggerName(activity.value);
        var title;
        var subtext;
        if (isTriggerChange) {
            var nextActivity = activities.find(function (_a) {
                var previousValue = _a.previousValue;
                return previousValue === activity.value;
            }) ||
                (activity.value &&
                    activity.value === "" + types_1.IncidentStatus.OPENED &&
                    activities.find(function (_a) {
                        var type = _a.type;
                        return type === types_1.IncidentActivityType.DETECTED;
                    }));
            var activityDuration = (nextActivity ? moment_timezone_1.default(nextActivity.dateCreated) : moment_timezone_1.default()).diff(moment_timezone_1.default(activity.dateCreated), 'milliseconds');
            title = locale_1.t('Alert status changed');
            subtext =
                activityDuration !== null &&
                    locale_1.tct("[currentTrigger]: [duration]", {
                        currentTrigger: currentTrigger,
                        duration: <duration_1.default abbreviation seconds={activityDuration / 1000}/>,
                    });
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === types_1.IncidentStatusMethod.RULE_UPDATED) {
            title = locale_1.t('Alert auto-resolved');
            subtext = locale_1.t('Alert rule modified or deleted');
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== types_1.IncidentStatusMethod.RULE_UPDATED) {
            title = locale_1.t('Resolved');
            subtext = locale_1.tct('by [authorName]', { authorName: authorName });
        }
        else if (isDetected) {
            title = (incident === null || incident === void 0 ? void 0 : incident.alertRule)
                ? locale_1.t('Alert was created')
                : locale_1.tct('[authorName] created an alert', { authorName: authorName });
            subtext = <dateTime_1.default timeOnly date={activity.dateCreated}/>;
        }
        else if (isStarted) {
            var dateEnded = moment_timezone_1.default(activity.dateCreated)
                .add(rule.timeWindow, 'minutes')
                .utc()
                .format();
            var timeOnly = Boolean(dateEnded && moment_timezone_1.default(activity.dateCreated).date() === moment_timezone_1.default(dateEnded).date());
            title = locale_1.t('Trigger conditions were met');
            subtext = (<React.Fragment>
          <dateTime_1.default timeOnly={timeOnly} timeAndDate={!timeOnly} date={activity.dateCreated}/>
          {' — '}
          <dateTime_1.default timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
        </React.Fragment>);
        }
        else {
            return null;
        }
        return (<Activity key={activity.id}>
        <ActivityTrack>{!last && <VerticalDivider />}</ActivityTrack>

        <ActivityBody>
          <ActivityTime>
            <StyledTimeSince date={activity.dateCreated} suffix={locale_1.t('ago')}/>
            <HorizontalDivider />
          </ActivityTime>
          <ActivityText>
            {title}
            {subtext && <ActivitySubText>{subtext}</ActivitySubText>}
          </ActivityText>
        </ActivityBody>
      </Activity>);
    };
    TimelineIncident.prototype.render = function () {
        var _this = this;
        var _a = this.props, incident = _a.incident, organization = _a.organization;
        return (<IncidentSection key={incident.identifier}>
        <IncidentHeader>
          <link_1.default to={{
                pathname: details_1.alertDetailsLink(organization, incident),
                query: { alert: incident.identifier },
            }}>
            {locale_1.tct('Alert #[id]', { id: incident.identifier })}
          </link_1.default>
          <SeenByTab>
            {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={locale_1.t('People who have viewed this alert')}/>)}
          </SeenByTab>
        </IncidentHeader>
        {incident.activities && (<IncidentBody>
            {incident.activities
                    .filter(function (activity) { return activity.type !== types_1.IncidentActivityType.COMMENT; })
                    .map(function (activity, idx) { return _this.renderActivity(activity, idx); })}
          </IncidentBody>)}
      </IncidentSection>);
    };
    return TimelineIncident;
}(React.Component));
var Timeline = /** @class */ (function (_super) {
    tslib_1.__extends(Timeline, _super);
    function Timeline() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<StyledEmptyStateWarning small withIcon={false}>
        <p>{locale_1.t('No alerts triggered during this time')}</p>
      </StyledEmptyStateWarning>);
        };
        return _this;
    }
    Timeline.prototype.render = function () {
        var _a = this.props, api = _a.api, incidents = _a.incidents, organization = _a.organization, rule = _a.rule;
        return (<History>
        <styles_1.SectionHeading>{locale_1.t('History')}</styles_1.SectionHeading>
        <ScrollPanel>
          <panels_1.PanelBody withPadding>
            {incidents && rule && incidents.length
                ? incidents.map(function (incident) { return (<TimelineIncident key={incident.identifier} api={api} organization={organization} incident={incident} rule={rule}/>); })
                : this.renderEmptyMessage()}
          </panels_1.PanelBody>
        </ScrollPanel>
      </History>);
    };
    return Timeline;
}(React.Component));
exports.default = Timeline;
var History = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 30px;\n"], ["\n  margin-bottom: 30px;\n"])));
var ScrollPanel = styled_1.default(panels_1.Panel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  max-height: 500px;\n  overflow: scroll;\n  -ms-overflow-style: none;\n  scrollbar-width: none;\n  &::-webkit-scrollbar {\n    display: none;\n  }\n\n  p {\n    font-size: ", ";\n  }\n"], ["\n  max-height: 500px;\n  overflow: scroll;\n  -ms-overflow-style: none;\n  scrollbar-width: none;\n  &::-webkit-scrollbar {\n    display: none;\n  }\n\n  p {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var IncidentSection = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  &:not(:first-of-type) {\n    margin-top: 15px;\n  }\n"], ["\n  &:not(:first-of-type) {\n    margin-top: 15px;\n  }\n"])));
var IncidentHeader = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var SeenByTab = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"], ["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"])), space_1.default(2));
var StyledSeenByList = styled_1.default(seenByList_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var IncidentBody = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Activity = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var ActivityTrack = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n\n  &:before {\n    content: '';\n    width: ", ";\n    height: ", ";\n    background-color: ", ";\n    border-radius: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n\n  &:before {\n    content: '';\n    width: ", ";\n    height: ", ";\n    background-color: ", ";\n    border-radius: ", ";\n  }\n"])), space_1.default(1), space_1.default(1), space_1.default(1), function (p) { return p.theme.gray300; }, space_1.default(1));
var ActivityBody = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"], ["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"])));
var ActivityTime = styled_1.default('li')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var ActivityText = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  flex-direction: row;\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  flex-direction: row;\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space_1.default(1.5), function (p) { return p.theme.fontSizeMedium; });
var ActivitySubText = styled_1.default('span')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5));
var HorizontalDivider = styled_1.default('div')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"], ["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"])), function (p) { return p.theme.innerBorder; });
var VerticalDivider = styled_1.default('div')(templateObject_17 || (templateObject_17 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"], ["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"])), function (p) { return p.theme.innerBorder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=timeline.jsx.map