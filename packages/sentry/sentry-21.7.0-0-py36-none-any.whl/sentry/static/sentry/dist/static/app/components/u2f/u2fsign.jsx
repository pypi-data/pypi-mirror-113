Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var u2finterface_1 = tslib_1.__importDefault(require("./u2finterface"));
var MESSAGES = {
    signin: locale_1.t('Insert your U2F device or tap the button on it to confirm the sign-in request.'),
    sudo: locale_1.t('Alternatively you can use your U2F device to confirm the action.'),
    enroll: locale_1.t('To enroll your U2F device insert it now or tap the button on it to activate it.'),
};
var U2fSign = /** @class */ (function (_super) {
    tslib_1.__extends(U2fSign, _super);
    function U2fSign() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    U2fSign.prototype.render = function () {
        var _a = this.props, displayMode = _a.displayMode, props = tslib_1.__rest(_a, ["displayMode"]);
        var flowMode = displayMode === 'enroll' ? 'enroll' : 'sign';
        return (<u2finterface_1.default {...props} silentIfUnsupported={displayMode === 'sudo'} flowMode={flowMode}>
        <p>{MESSAGES[displayMode] || null}</p>
      </u2finterface_1.default>);
    };
    U2fSign.defaultProps = {
        displayMode: 'signin',
    };
    return U2fSign;
}(react_1.Component));
exports.default = U2fSign;
//# sourceMappingURL=u2fsign.jsx.map