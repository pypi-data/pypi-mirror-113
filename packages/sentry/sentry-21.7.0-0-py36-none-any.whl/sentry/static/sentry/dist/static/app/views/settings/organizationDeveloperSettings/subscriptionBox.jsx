Object.defineProperty(exports, "__esModule", { value: true });
exports.SubscriptionBox = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var constants_1 = require("app/views/settings/organizationDeveloperSettings/constants");
var SubscriptionBox = /** @class */ (function (_super) {
    tslib_1.__extends(SubscriptionBox, _super);
    function SubscriptionBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (evt) {
            var checked = evt.target.checked;
            var resource = _this.props.resource;
            _this.props.onChange(resource, checked);
        };
        return _this;
    }
    SubscriptionBox.prototype.render = function () {
        var _a = this.props, resource = _a.resource, organization = _a.organization, webhookDisabled = _a.webhookDisabled, checked = _a.checked;
        var features = new Set(organization.features);
        var disabled = this.props.disabledFromPermissions || webhookDisabled;
        var message = "Must have at least 'Read' permissions enabled for " + resource;
        if (resource === 'error' && !features.has('integrations-event-hooks')) {
            disabled = true;
            message =
                'Your organization does not have access to the error subscription resource.';
        }
        if (webhookDisabled) {
            message = 'Cannot enable webhook subscription without specifying a webhook url';
        }
        return (<React.Fragment>
        <SubscriptionGridItemWrapper key={resource}>
          <tooltip_1.default disabled={!disabled} title={message}>
            <SubscriptionGridItem disabled={disabled}>
              <SubscriptionInfo>
                <SubscriptionTitle>{locale_1.t("" + resource)}</SubscriptionTitle>
                <SubscriptionDescription>
                  {locale_1.t("" + constants_1.DESCRIPTIONS[resource])}
                </SubscriptionDescription>
              </SubscriptionInfo>
              <checkbox_1.default key={"" + resource + checked} disabled={disabled} id={resource} value={resource} checked={checked} onChange={this.onChange}/>
            </SubscriptionGridItem>
          </tooltip_1.default>
        </SubscriptionGridItemWrapper>
      </React.Fragment>);
    };
    SubscriptionBox.defaultProps = {
        webhookDisabled: false,
    };
    return SubscriptionBox;
}(React.Component));
exports.SubscriptionBox = SubscriptionBox;
exports.default = withOrganization_1.default(SubscriptionBox);
var SubscriptionInfo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var SubscriptionGridItem = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  background: ", ";\n  opacity: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  background: ", ";\n  opacity: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"])), function (p) { return p.theme.backgroundSecondary; }, function (_a) {
    var disabled = _a.disabled;
    return (disabled ? 0.3 : 1);
});
var SubscriptionGridItemWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 12px;\n  width: 33%;\n"], ["\n  padding: 12px;\n  width: 33%;\n"])));
var SubscriptionDescription = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 12px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n"], ["\n  font-size: 12px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.gray300; });
var SubscriptionTitle = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: 16px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n  margin-bottom: 5px;\n"], ["\n  font-size: 16px;\n  line-height: 1;\n  color: ", ";\n  white-space: nowrap;\n  margin-bottom: 5px;\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=subscriptionBox.jsx.map