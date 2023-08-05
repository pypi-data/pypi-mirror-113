Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var platformExternalIssues_1 = require("app/actionCreators/platformExternalIssues");
var issueSyncListElement_1 = require("app/components/issueSyncListElement");
var sentryAppIcon_1 = require("app/components/sentryAppIcon");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var sentryAppExternalIssueModal_1 = tslib_1.__importDefault(require("./sentryAppExternalIssueModal"));
var SentryAppExternalIssueActions = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppExternalIssueActions, _super);
    function SentryAppExternalIssueActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            action: 'create',
            externalIssue: _this.props.externalIssue,
        };
        _this.doOpenModal = function (e) {
            // Only show the modal when we don't have a linked issue
            if (_this.state.externalIssue) {
                return;
            }
            var _a = _this.props, group = _a.group, event = _a.event, sentryAppComponent = _a.sentryAppComponent, sentryAppInstallation = _a.sentryAppInstallation;
            recordSentryAppInteraction_1.recordInteraction(sentryAppComponent.sentryApp.slug, 'sentry_app_component_interacted', {
                componentType: 'issue-link',
            });
            e === null || e === void 0 ? void 0 : e.preventDefault();
            modal_1.openModal(function (deps) { return (<sentryAppExternalIssueModal_1.default {...deps} {...{ group: group, event: event, sentryAppComponent: sentryAppComponent, sentryAppInstallation: sentryAppInstallation }} onSubmitSuccess={_this.onSubmitSuccess}/>); });
        };
        _this.deleteIssue = function () {
            var _a = _this.props, api = _a.api, group = _a.group;
            var externalIssue = _this.state.externalIssue;
            externalIssue &&
                platformExternalIssues_1.deleteExternalIssue(api, group.id, externalIssue.id)
                    .then(function (_data) {
                    _this.setState({ externalIssue: undefined });
                    indicator_1.addSuccessMessage(locale_1.t('Successfully unlinked issue.'));
                })
                    .catch(function (_error) {
                    indicator_1.addErrorMessage(locale_1.t('Unable to unlink issue.'));
                });
        };
        _this.onAddRemoveClick = function () {
            var externalIssue = _this.state.externalIssue;
            if (!externalIssue) {
                _this.doOpenModal();
            }
            else {
                _this.deleteIssue();
            }
        };
        _this.onSubmitSuccess = function (externalIssue) {
            _this.setState({ externalIssue: externalIssue });
        };
        return _this;
    }
    SentryAppExternalIssueActions.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.externalIssue !== prevProps.externalIssue) {
            this.updateExternalIssue(this.props.externalIssue);
        }
    };
    SentryAppExternalIssueActions.prototype.updateExternalIssue = function (externalIssue) {
        this.setState({ externalIssue: externalIssue });
    };
    SentryAppExternalIssueActions.prototype.render = function () {
        var sentryAppComponent = this.props.sentryAppComponent;
        var externalIssue = this.state.externalIssue;
        var name = sentryAppComponent.sentryApp.name;
        var url = '#';
        var displayName = locale_1.tct('Link [name] Issue', { name: name });
        if (externalIssue) {
            url = externalIssue.webUrl;
            displayName = externalIssue.displayName;
        }
        return (<IssueLinkContainer>
        <IssueLink>
          <StyledSentryAppIcon slug={sentryAppComponent.sentryApp.slug}/>
          <issueSyncListElement_1.IntegrationLink onClick={this.doOpenModal} href={url}>
            {displayName}
          </issueSyncListElement_1.IntegrationLink>
        </IssueLink>
        <StyledIcon onClick={this.onAddRemoveClick}>
          {!!externalIssue ? <icons_1.IconClose /> : <icons_1.IconAdd />}
        </StyledIcon>
      </IssueLinkContainer>);
    };
    return SentryAppExternalIssueActions;
}(React.Component));
var StyledSentryAppIcon = styled_1.default(sentryAppIcon_1.SentryAppIcon)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"])), function (p) { return p.theme.textColor; }, space_1.default(3), space_1.default(3));
var IssueLink = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"])));
var IssueLinkContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"])));
var StyledIcon = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n"], ["\n  color: ", ";\n  cursor: pointer;\n"])), function (p) { return p.theme.textColor; });
exports.default = withApi_1.default(SentryAppExternalIssueActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryAppExternalIssueActions.jsx.map