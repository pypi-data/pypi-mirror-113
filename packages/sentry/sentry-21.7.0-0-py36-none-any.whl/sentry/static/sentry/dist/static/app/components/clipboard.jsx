Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var copy_text_to_clipboard_1 = tslib_1.__importDefault(require("copy-text-to-clipboard"));
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
/**
 * copy-text-to-clipboard relies on `document.execCommand('copy')`
 */
function isSupported() {
    var support = !!document.queryCommandSupported;
    return support && !!document.queryCommandSupported('copy');
}
var Clipboard = /** @class */ (function (_super) {
    tslib_1.__extends(Clipboard, _super);
    function Clipboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            var _a = _this.props, value = _a.value, hideMessages = _a.hideMessages, successMessage = _a.successMessage, errorMessage = _a.errorMessage, onSuccess = _a.onSuccess, onError = _a.onError;
            // Copy returns whether it succeeded to copy the text
            var success = copy_text_to_clipboard_1.default(value);
            if (!success) {
                if (!hideMessages) {
                    indicator_1.addErrorMessage(errorMessage);
                }
                onError === null || onError === void 0 ? void 0 : onError();
                return;
            }
            if (!hideMessages) {
                indicator_1.addSuccessMessage(successMessage);
            }
            onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
        };
        _this.handleMount = function (ref) {
            var _a;
            if (!ref) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            _this.element = react_dom_1.default.findDOMNode(ref);
            (_a = _this.element) === null || _a === void 0 ? void 0 : _a.addEventListener('click', _this.handleClick);
        };
        return _this;
    }
    Clipboard.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.element) === null || _a === void 0 ? void 0 : _a.removeEventListener('click', this.handleClick);
    };
    Clipboard.prototype.render = function () {
        var _a = this.props, children = _a.children, hideUnsupported = _a.hideUnsupported;
        // Browser doesn't support `execCommand`
        if (hideUnsupported && !isSupported()) {
            return null;
        }
        if (!react_1.isValidElement(children)) {
            return null;
        }
        return react_1.cloneElement(children, {
            ref: this.handleMount,
        });
    };
    Clipboard.defaultProps = {
        hideMessages: false,
        successMessage: locale_1.t('Copied to clipboard'),
        errorMessage: locale_1.t('Error copying to clipboard'),
    };
    return Clipboard;
}(react_1.Component));
exports.default = Clipboard;
//# sourceMappingURL=clipboard.jsx.map