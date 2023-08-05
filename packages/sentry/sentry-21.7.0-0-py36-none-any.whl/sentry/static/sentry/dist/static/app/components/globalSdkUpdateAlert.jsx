Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var prompts_1 = require("app/actionCreators/prompts");
var sidebarPanelActions_1 = tslib_1.__importDefault(require("app/actions/sidebarPanelActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var promptIsDismissed_1 = require("app/utils/promptIsDismissed");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withSdkUpdates_1 = tslib_1.__importDefault(require("app/utils/withSdkUpdates"));
var types_1 = require("./sidebar/types");
var button_1 = tslib_1.__importDefault(require("./button"));
var recordAnalyticsSeen = function (_a) {
    var organization = _a.organization;
    return analytics_1.trackAnalyticsEvent({
        eventKey: 'sdk_updates.seen',
        eventName: 'SDK Updates: Seen',
        organization_id: organization.id,
    });
};
var recordAnalyticsSnoozed = function (_a) {
    var organization = _a.organization;
    return analytics_1.trackAnalyticsEvent({
        eventKey: 'sdk_updates.snoozed',
        eventName: 'SDK Updates: Snoozed',
        organization_id: organization.id,
    });
};
var recordAnalyticsClicked = function (_a) {
    var organization = _a.organization;
    return analytics_1.trackAnalyticsEvent({
        eventKey: 'sdk_updates.clicked',
        eventName: 'SDK Updates: Clicked',
        organization_id: organization.id,
    });
};
var flattenSuggestions = function (list) {
    return list.reduce(function (suggestions, sdk) { return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(suggestions)), tslib_1.__read(sdk.suggestions)); }, []);
};
var InnerGlobalSdkSuggestions = /** @class */ (function (_super) {
    tslib_1.__extends(InnerGlobalSdkSuggestions, _super);
    function InnerGlobalSdkSuggestions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isDismissed: null,
        };
        _this.snoozePrompt = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            prompts_1.promptsUpdate(api, {
                organizationId: organization.id,
                feature: 'sdk_updates',
                status: 'snoozed',
            });
            _this.setState({ isDismissed: true });
            recordAnalyticsSnoozed({ organization: _this.props.organization });
        };
        return _this;
    }
    InnerGlobalSdkSuggestions.prototype.componentDidMount = function () {
        this.promptsCheck();
        recordAnalyticsSeen({ organization: this.props.organization });
    };
    InnerGlobalSdkSuggestions.prototype.promptsCheck = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, prompt;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, prompts_1.promptsCheck(api, {
                                organizationId: organization.id,
                                feature: 'sdk_updates',
                            })];
                    case 1:
                        prompt = _b.sent();
                        this.setState({
                            isDismissed: promptIsDismissed_1.promptIsDismissed(prompt),
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    InnerGlobalSdkSuggestions.prototype.render = function () {
        var _a = this.props, _api = _a.api, selection = _a.selection, sdkUpdates = _a.sdkUpdates, organization = _a.organization, Wrapper = _a.Wrapper, props = tslib_1.__rest(_a, ["api", "selection", "sdkUpdates", "organization", "Wrapper"]);
        var isDismissed = this.state.isDismissed;
        if (!sdkUpdates || isDismissed === null || isDismissed) {
            return null;
        }
        // withSdkUpdates explicitly only queries My Projects. This means that when
        // looking at any projects outside of My Projects (like All Projects), this
        // will only show the updates relevant to the to user.
        var projectSpecificUpdates = (selection === null || selection === void 0 ? void 0 : selection.projects.length) === 0 || (selection === null || selection === void 0 ? void 0 : selection.projects) === [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            ? sdkUpdates
            : sdkUpdates.filter(function (update) { var _a; return (_a = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _a === void 0 ? void 0 : _a.includes(parseInt(update.projectId, 10)); });
        // Are there any updates?
        if (flattenSuggestions(projectSpecificUpdates).length === 0) {
            return null;
        }
        var showBroadcastsPanel = (<button_1.default priority="link" onClick={function () {
                sidebarPanelActions_1.default.activatePanel(types_1.SidebarPanelKey.Broadcasts);
                recordAnalyticsClicked({ organization: organization });
            }}>
        {locale_1.t('Review updates')}
      </button_1.default>);
        var notice = (<alert_1.default type="info" icon={<icons_1.IconUpgrade />} {...props}>
        <Content>
          {locale_1.t("You have outdated SDKs in your projects. Update them for important fixes and features.")}
          <Actions>
            <button_1.default priority="link" title={locale_1.t('Dismiss for the next two weeks')} onClick={this.snoozePrompt}>
              {locale_1.t('Remind me later')}
            </button_1.default>
            |{showBroadcastsPanel}
          </Actions>
        </Content>
      </alert_1.default>);
        return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
    };
    return InnerGlobalSdkSuggestions;
}(React.Component));
var Content = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var Actions = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, max-content);\n  grid-gap: ", ";\n"])), space_1.default(1));
var GlobalSdkSuggestions = withOrganization_1.default(withSdkUpdates_1.default(withGlobalSelection_1.default(withApi_1.default(InnerGlobalSdkSuggestions))));
exports.default = GlobalSdkSuggestions;
var templateObject_1, templateObject_2;
//# sourceMappingURL=globalSdkUpdateAlert.jsx.map