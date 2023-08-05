Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var codesworth_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/codesworth.svg"));
var prompts_1 = require("app/actionCreators/prompts");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var commitRow_1 = tslib_1.__importDefault(require("app/components/commitRow"));
var styles_1 = require("app/components/events/styles");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var analytics_1 = require("app/utils/analytics");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var EXAMPLE_COMMITS = ['dec0de', 'de1e7e', '5ca1ed'];
var DUMMY_COMMIT = {
    id: getDynamicText_1.default({
        value: EXAMPLE_COMMITS[Math.floor(Math.random() * EXAMPLE_COMMITS.length)],
        fixed: '5ca1ed',
    }),
    author: {
        id: '',
        name: 'codesworth',
        username: '',
        email: 'codesworth@example.com',
        ip_address: '',
        lastSeen: '',
        lastLogin: '',
        isSuperuser: false,
        isAuthenticated: false,
        emails: [],
        isManaged: false,
        lastActive: '',
        isStaff: false,
        identities: [],
        isActive: true,
        has2fa: false,
        canReset2fa: false,
        authenticators: [],
        dateJoined: '',
        options: {
            theme: 'system',
            timezone: '',
            stacktraceOrder: 1,
            language: '',
            clock24Hours: false,
            avatarType: 'letter_avatar',
        },
        flags: { newsletter_consent_prompt: false },
        hasPasswordAuth: true,
        permissions: new Set([]),
        experiments: {},
    },
    dateCreated: moment_1.default().subtract(3, 'day').format(),
    repository: {
        id: '',
        integrationId: '',
        name: '',
        externalSlug: '',
        url: '',
        provider: {
            id: 'integrations:github',
            name: 'GitHub',
        },
        dateCreated: '',
        status: types_1.RepositoryStatus.ACTIVE,
    },
    releases: [],
    message: locale_1.t('This example commit broke something'),
};
var SUSPECT_COMMITS_FEATURE = 'suspect_commits';
var EventCauseEmpty = /** @class */ (function (_super) {
    tslib_1.__extends(EventCauseEmpty, _super);
    function EventCauseEmpty() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: undefined,
        };
        return _this;
    }
    EventCauseEmpty.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventCauseEmpty.prototype.componentDidUpdate = function (_prevProps, prevState) {
        var _a = this.props, project = _a.project, organization = _a.organization;
        var shouldShow = this.state.shouldShow;
        if (!prevState.shouldShow && shouldShow) {
            // send to reload only due to high event volume
            analytics_1.trackAdhocEvent({
                eventKey: 'event_cause.viewed',
                org_id: parseInt(organization.id, 10),
                project_id: parseInt(project.id, 10),
                platform: project.platform,
            });
        }
    };
    EventCauseEmpty.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, event, project, organization, data;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, event = _a.event, project = _a.project, organization = _a.organization;
                        if (!promptIsDismissed_1.promptCanShow(SUSPECT_COMMITS_FEATURE, event.eventID)) {
                            this.setState({ shouldShow: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                projectId: project.id,
                                organizationId: organization.id,
                                feature: SUSPECT_COMMITS_FEATURE,
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: !promptIsDismissed_1.promptIsDismissed(data !== null && data !== void 0 ? data : {}, 7) });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventCauseEmpty.prototype.handleClick = function (_a) {
        var _this = this;
        var action = _a.action, eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, api = _b.api, project = _b.project, organization = _b.organization;
        var data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: SUSPECT_COMMITS_FEATURE,
            status: action,
        };
        prompts_1.promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        this.trackAnalytics({ eventKey: eventKey, eventName: eventName });
    };
    EventCauseEmpty.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, project = _b.project, organization = _b.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    };
    EventCauseEmpty.prototype.render = function () {
        var _this = this;
        var shouldShow = this.state.shouldShow;
        if (!shouldShow) {
            return null;
        }
        return (<styles_1.DataSection data-test-id="loaded-event-cause-empty">
        <StyledPanel dashedBorder>
          <BoxHeader>
            <Description>
              <h3>{locale_1.t('Configure Suspect Commits')}</h3>
              <p>{locale_1.t('To identify which commit caused this issue')}</p>
            </Description>
            <ButtonList>
              <DocsButton size="small" priority="primary" href="https://docs.sentry.io/product/releases/setup/" onClick={function () {
                return _this.trackAnalytics({
                    eventKey: 'event_cause.docs_clicked',
                    eventName: 'Event Cause Docs Clicked',
                });
            }}>
                {locale_1.t('Read the docs')}
              </DocsButton>

              <div>
                <SnoozeButton title={locale_1.t('Remind me next week')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'snoozed',
                    eventKey: 'event_cause.snoozed',
                    eventName: 'Event Cause Snoozed',
                });
            }}>
                  {locale_1.t('Snooze')}
                </SnoozeButton>
                <DismissButton title={locale_1.t('Dismiss for this project')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'dismissed',
                    eventKey: 'event_cause.dismissed',
                    eventName: 'Event Cause Dismissed',
                });
            }}>
                  {locale_1.t('Dismiss')}
                </DismissButton>
              </div>
            </ButtonList>
          </BoxHeader>
          <ExampleCommitPanel>
            <commitRow_1.default key={DUMMY_COMMIT.id} commit={DUMMY_COMMIT} customAvatar={<CustomAvatar src={codesworth_svg_1.default}/>}/>
          </ExampleCommitPanel>
        </StyledPanel>
      </styles_1.DataSection>);
    };
    return EventCauseEmpty;
}(react_1.Component));
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  padding-bottom: 0;\n  background: none;\n"], ["\n  padding: ", ";\n  padding-bottom: 0;\n  background: none;\n"])), space_1.default(3));
var Description = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"])), space_1.default(0.25), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; }, space_1.default(1.5));
var ButtonList = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"])), space_1.default(1));
var DocsButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.white; });
var SnoozeButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  border-right: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  border-right: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"])));
var DismissButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"], ["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"])));
var ExampleCommitPanel = styled_1.default(panels_1.Panel)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  pointer-events: none;\n  position: relative;\n  padding-right: ", ";\n\n  &:after {\n    display: block;\n    content: 'Example';\n    position: absolute;\n    top: 16px;\n    right: -24px;\n    text-transform: uppercase;\n    background: #e46187;\n    padding: 4px 26px;\n    line-height: 11px;\n    font-size: 11px;\n    color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  overflow: hidden;\n  pointer-events: none;\n  position: relative;\n  padding-right: ", ";\n\n  &:after {\n    display: block;\n    content: 'Example';\n    position: absolute;\n    top: 16px;\n    right: -24px;\n    text-transform: uppercase;\n    background: #e46187;\n    padding: 4px 26px;\n    line-height: 11px;\n    font-size: 11px;\n    color: ", ";\n    transform: rotate(45deg);\n  }\n"])), space_1.default(3), function (p) { return p.theme.white; });
var CustomAvatar = styled_1.default('img')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  height: 48px;\n  padding-right: 12px;\n  margin: -6px 0px -6px -2px;\n"], ["\n  height: 48px;\n  padding-right: 12px;\n  margin: -6px 0px -6px -2px;\n"])));
var BoxHeader = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"], ["\n  display: grid;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"])));
exports.default = withApi_1.default(EventCauseEmpty);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=eventCauseEmpty.jsx.map