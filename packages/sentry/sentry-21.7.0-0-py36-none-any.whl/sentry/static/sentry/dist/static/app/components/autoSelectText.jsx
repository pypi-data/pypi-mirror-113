Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var isRenderFunc_1 = require("app/utils/isRenderFunc");
var selectText_1 = require("app/utils/selectText");
var AutoSelectText = /** @class */ (function (_super) {
    tslib_1.__extends(AutoSelectText, _super);
    function AutoSelectText() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.selectText = function () {
            if (!_this.el) {
                return;
            }
            selectText_1.selectText(_this.el);
        };
        _this.handleMount = function (el) {
            _this.el = el;
        };
        return _this;
    }
    AutoSelectText.prototype.render = function () {
        var _a = this.props, children = _a.children, className = _a.className, props = tslib_1.__rest(_a, ["children", "className"]);
        if (isRenderFunc_1.isRenderFunc(children)) {
            return children({
                doMount: this.handleMount,
                doSelect: this.selectText,
            });
        }
        // use an inner span here for the selection as otherwise the selectText
        // function will create a range that includes the entire part of the
        // div (including the div itself) which causes newlines to be selected
        // in chrome.
        return (<div {...props} onClick={this.selectText} className={classnames_1.default('auto-select-text', className)}>
        <span ref={this.handleMount}>{children}</span>
      </div>);
    };
    return AutoSelectText;
}(React.Component));
exports.default = AutoSelectText;
//# sourceMappingURL=autoSelectText.jsx.map