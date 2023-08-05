Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var addIntegration_1 = tslib_1.__importDefault(require("./addIntegration"));
var AddIntegrationButton = /** @class */ (function (_super) {
    tslib_1.__extends(AddIntegrationButton, _super);
    function AddIntegrationButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AddIntegrationButton.prototype.render = function () {
        var _a = this.props, provider = _a.provider, buttonText = _a.buttonText, onAddIntegration = _a.onAddIntegration, organization = _a.organization, reinstall = _a.reinstall, analyticsParams = _a.analyticsParams, modalParams = _a.modalParams, buttonProps = tslib_1.__rest(_a, ["provider", "buttonText", "onAddIntegration", "organization", "reinstall", "analyticsParams", "modalParams"]);
        var label = buttonText || locale_1.t(reinstall ? 'Enable' : 'Add %s', provider.metadata.noun);
        return (<tooltip_1.default disabled={provider.canAdd} title={"Integration cannot be added on Sentry. Enable this integration via the " + provider.name + " instance."}>
        <addIntegration_1.default provider={provider} onInstall={onAddIntegration} organization={organization} analyticsParams={analyticsParams} modalParams={modalParams}>
          {function (onClick) { return (<button_1.default disabled={!provider.canAdd} {...buttonProps} onClick={function () { return onClick(); }}>
              {label}
            </button_1.default>); }}
        </addIntegration_1.default>
      </tooltip_1.default>);
    };
    return AddIntegrationButton;
}(React.Component));
exports.default = AddIntegrationButton;
//# sourceMappingURL=addIntegrationButton.jsx.map