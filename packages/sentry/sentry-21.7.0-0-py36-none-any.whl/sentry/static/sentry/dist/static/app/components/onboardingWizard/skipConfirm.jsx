Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var locale_1 = require("app/locale");
var animations_1 = require("app/styles/animations");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SkipConfirm = /** @class */ (function (_super) {
    tslib_1.__extends(SkipConfirm, _super);
    function SkipConfirm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showConfirmation: false,
        };
        _this.toggleConfirm = function (e) {
            e.stopPropagation();
            _this.setState(function (state) { return ({ showConfirmation: !state.showConfirmation }); });
        };
        _this.handleSkip = function (e) {
            e.stopPropagation();
            _this.props.onSkip();
        };
        return _this;
    }
    SkipConfirm.prototype.render = function () {
        var children = this.props.children;
        return (<React.Fragment>
        {children({ skip: this.toggleConfirm })}
        <Confirmation visible={this.state.showConfirmation} onSkip={this.handleSkip} onDismiss={this.toggleConfirm}/>
      </React.Fragment>);
    };
    return SkipConfirm;
}(React.Component));
exports.default = SkipConfirm;
var SkipHelp = hookOrDefault_1.default({
    hookName: 'onboarding-wizard:skip-help',
    defaultComponent: function () { return (<button_1.default priority="primary" size="xsmall" to="https://forum.sentry.io/" external>
      {locale_1.t('Community Forum')}
    </button_1.default>); },
});
var Confirmation = styled_1.default(function (_a) {
    var onDismiss = _a.onDismiss, onSkip = _a.onSkip, _ = _a.visible, props = tslib_1.__rest(_a, ["onDismiss", "onSkip", "visible"]);
    return (<div onClick={onDismiss} {...props}>
    <p>{locale_1.t("Not sure what to do? We're here for you!")}</p>
    <buttonBar_1.default gap={1}>
      <SkipHelp />
      <button_1.default size="xsmall" onClick={onSkip}>
        {locale_1.t('Just skip')}
      </button_1.default>
    </buttonBar_1.default>
  </div>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n  padding: 0 ", ";\n  border-radius: ", ";\n  align-items: center;\n  flex-direction: column;\n  justify-content: center;\n  background: rgba(255, 255, 255, 0.9);\n  animation: ", " 200ms normal forwards;\n  font-size: ", ";\n\n  p {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  bottom: 0;\n  right: 0;\n  padding: 0 ", ";\n  border-radius: ", ";\n  align-items: center;\n  flex-direction: column;\n  justify-content: center;\n  background: rgba(255, 255, 255, 0.9);\n  animation: ", " 200ms normal forwards;\n  font-size: ", ";\n\n  p {\n    margin-bottom: ", ";\n  }\n"])), function (p) { return (p.visible ? 'flex' : 'none'); }, space_1.default(3), function (p) { return p.theme.borderRadius; }, animations_1.fadeIn, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1));
var templateObject_1;
//# sourceMappingURL=skipConfirm.jsx.map