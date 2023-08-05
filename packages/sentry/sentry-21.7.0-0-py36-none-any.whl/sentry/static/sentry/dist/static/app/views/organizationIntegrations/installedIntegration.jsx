Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationItem_1 = tslib_1.__importDefault(require("./integrationItem"));
var InstalledIntegration = /** @class */ (function (_super) {
    tslib_1.__extends(InstalledIntegration, _super);
    function InstalledIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUninstallClick = function () {
            _this.props.trackIntegrationEvent('integrations.uninstall_clicked');
        };
        return _this;
    }
    InstalledIntegration.prototype.getRemovalBodyAndText = function (aspects) {
        if (aspects && aspects.removal_dialog) {
            return {
                body: aspects.removal_dialog.body,
                actionText: aspects.removal_dialog.actionText,
            };
        }
        else {
            return {
                body: locale_1.t('Deleting this integration will remove any project associated data. This action cannot be undone. Are you sure you want to delete this integration?'),
                actionText: locale_1.t('Delete'),
            };
        }
    };
    InstalledIntegration.prototype.handleRemove = function (integration) {
        this.props.onRemove(integration);
        this.props.trackIntegrationEvent('integrations.uninstall_completed');
    };
    Object.defineProperty(InstalledIntegration.prototype, "removeConfirmProps", {
        get: function () {
            var _this = this;
            var integration = this.props.integration;
            var _a = this.getRemovalBodyAndText(integration.provider.aspects), body = _a.body, actionText = _a.actionText;
            var message = (<React.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.t('Deleting this integration has consequences!')}
        </alert_1.default>
        {body}
      </React.Fragment>);
            return {
                message: message,
                confirmText: actionText,
                onConfirm: function () { return _this.handleRemove(integration); },
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(InstalledIntegration.prototype, "disableConfirmProps", {
        get: function () {
            var _this = this;
            var integration = this.props.integration;
            var _a = integration.provider.aspects.disable_dialog || {}, body = _a.body, actionText = _a.actionText;
            var message = (<React.Fragment>
        <alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.t('This integration cannot be removed in Sentry')}
        </alert_1.default>
        {body}
      </React.Fragment>);
            return {
                message: message,
                confirmText: actionText,
                onConfirm: function () { return _this.props.onDisable(integration); },
            };
        },
        enumerable: false,
        configurable: true
    });
    InstalledIntegration.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, integration = _a.integration, provider = _a.provider, organization = _a.organization;
        var removeConfirmProps = integration.status === 'active' && integration.provider.canDisable
            ? this.disableConfirmProps
            : this.removeConfirmProps;
        return (<access_1.default access={['org:integrations']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<IntegrationFlex key={integration.id} className={className}>
            <IntegrationItemBox>
              <integrationItem_1.default integration={integration}/>
            </IntegrationItemBox>
            <div>
              <tooltip_1.default disabled={hasAccess} position="left" title={locale_1.t('You must be an organization owner, manager or admin to configure')}>
                <StyledButton borderless icon={<icons_1.IconSettings />} disabled={!hasAccess || integration.status !== 'active'} to={"/settings/" + organization.slug + "/integrations/" + provider.key + "/" + integration.id + "/"} data-test-id="integration-configure-button">
                  {locale_1.t('Configure')}
                </StyledButton>
              </tooltip_1.default>
            </div>
            <div>
              <tooltip_1.default disabled={hasAccess} title={locale_1.t('You must be an organization owner, manager or admin to uninstall')}>
                <confirm_1.default priority="danger" onConfirming={_this.handleUninstallClick} disabled={!hasAccess} {...removeConfirmProps}>
                  <StyledButton disabled={!hasAccess} borderless icon={<icons_1.IconDelete />} data-test-id="integration-remove-button">
                    {locale_1.t('Uninstall')}
                  </StyledButton>
                </confirm_1.default>
              </tooltip_1.default>
            </div>

            <StyledIntegrationStatus status={integration.status}/>
          </IntegrationFlex>);
            }}
      </access_1.default>);
    };
    return InstalledIntegration;
}(React.Component));
exports.default = InstalledIntegration;
var StyledButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var IntegrationFlex = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationItemBox = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var IntegrationStatus = react_1.withTheme(function (props) {
    var theme = props.theme, status = props.status, p = tslib_1.__rest(props, ["theme", "status"]);
    var color = status === 'active' ? theme.success : theme.gray300;
    var titleText = status === 'active'
        ? locale_1.t('This Integration can be disabled by clicking the Uninstall button')
        : locale_1.t('This Integration has been disconnected from the external provider');
    return (<tooltip_1.default title={titleText}>
        <div {...p}>
          <circleIndicator_1.default size={6} color={color}/>
          <IntegrationStatusText>{"" + (status === 'active' ? locale_1.t('enabled') : locale_1.t('disabled'))}</IntegrationStatusText>
        </div>
      </tooltip_1.default>);
});
var StyledIntegrationStatus = styled_1.default(IntegrationStatus)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-weight: light;\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-weight: light;\n  text-transform: capitalize;\n  &:before {\n    content: '|';\n    color: ", ";\n    margin-right: ", ";\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.gray200; }, space_1.default(1));
var IntegrationStatusText = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", " 0 ", ";\n"], ["\n  margin: 0 ", " 0 ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=installedIntegration.jsx.map