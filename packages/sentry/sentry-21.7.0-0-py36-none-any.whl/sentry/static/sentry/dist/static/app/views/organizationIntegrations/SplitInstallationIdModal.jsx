Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
/**
 * This component is a hack for Split.
 * It will display the installation ID after installation so users can copy it and paste it in Split's website.
 * We also have a link for users to click so they can go to Split's website.
 */
var SplitInstallationIdModal = /** @class */ (function (_super) {
    tslib_1.__extends(SplitInstallationIdModal, _super);
    function SplitInstallationIdModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onCopy = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () { return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: 
                // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
                return [4 /*yield*/, navigator.clipboard.writeText(this.props.installationId)];
                case 1: 
                // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
                return [2 /*return*/, _a.sent()];
            }
        }); }); };
        _this.handleContinue = function () {
            var delay = 2000;
            _this.onCopy();
            indicator_1.addSuccessMessage('Copied to clipboard');
            setTimeout(function () {
                window.open('https://app.split.io/org/admin/integrations');
            }, delay);
        };
        return _this;
    }
    SplitInstallationIdModal.prototype.render = function () {
        var _a = this.props, installationId = _a.installationId, closeModal = _a.closeModal;
        // no need to translate this temporary component
        return (<div>
        <ItemHolder>
          Copy this Installation ID and click to continue. You will use it to finish setup
          on Split.io.
        </ItemHolder>
        <ItemHolder>
          <textCopyInput_1.default onCopy={this.onCopy}>{installationId}</textCopyInput_1.default>
        </ItemHolder>
        <ButtonHolder>
          <button_1.default size="small" onClick={closeModal}>
            Close
          </button_1.default>
          <button_1.default size="small" priority="primary" onClick={this.handleContinue}>
            Copy and Open Link
          </button_1.default>
        </ButtonHolder>
      </div>);
    };
    return SplitInstallationIdModal;
}(react_1.Component));
exports.default = SplitInstallationIdModal;
var ItemHolder = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: 10px;\n"], ["\n  margin: 10px;\n"])));
var ButtonHolder = styled_1.default(ItemHolder)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  & button {\n    margin: 5px;\n  }\n"], ["\n  text-align: right;\n  & button {\n    margin: 5px;\n  }\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=SplitInstallationIdModal.jsx.map