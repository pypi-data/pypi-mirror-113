Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var icons_1 = require("app/icons");
var input_1 = require("app/styles/input");
var selectText_1 = require("app/utils/selectText");
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledInput = styled_1.default('input')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  background-color: ", ";\n  border-right-width: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n  direction: ", ";\n\n  &:hover,\n  &:focus {\n    background-color: ", ";\n    border-right-width: 0;\n  }\n"], ["\n  ", ";\n  background-color: ", ";\n  border-right-width: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n  direction: ", ";\n\n  &:hover,\n  &:focus {\n    background-color: ", ";\n    border-right-width: 0;\n  }\n"])), input_1.inputStyles, function (p) { return p.theme.backgroundSecondary; }, function (p) { return (p.rtl ? 'rtl' : 'ltr'); }, function (p) { return p.theme.backgroundSecondary; });
var OverflowContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  border: none;\n"], ["\n  flex-grow: 1;\n  border: none;\n"])));
var StyledCopyButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  border-radius: 0 0.25em 0.25em 0;\n  box-shadow: none;\n"], ["\n  flex-shrink: 1;\n  border-radius: 0 0.25em 0.25em 0;\n  box-shadow: none;\n"])));
var TextCopyInput = /** @class */ (function (_super) {
    tslib_1.__extends(TextCopyInput, _super);
    function TextCopyInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.textRef = React.createRef();
        // Select text when copy button is clicked
        _this.handleCopyClick = function (e) {
            if (!_this.textRef.current) {
                return;
            }
            var _a = _this.props, onCopy = _a.onCopy, children = _a.children;
            _this.handleSelectText();
            onCopy === null || onCopy === void 0 ? void 0 : onCopy(children, e);
            e.stopPropagation();
        };
        _this.handleSelectText = function () {
            var rtl = _this.props.rtl;
            if (!_this.textRef.current) {
                return;
            }
            // We use findDOMNode here because `this.textRef` is not a dom node,
            // it's a ref to AutoSelectText
            var node = react_dom_1.default.findDOMNode(_this.textRef.current); // eslint-disable-line react/no-find-dom-node
            if (!node || !(node instanceof HTMLElement)) {
                return;
            }
            if (rtl && node instanceof HTMLInputElement) {
                // we don't want to select the first character - \u202A, nor the last - \u202C
                node.setSelectionRange(1, node.value.length - 1);
            }
            else {
                selectText_1.selectText(node);
            }
        };
        return _this;
    }
    TextCopyInput.prototype.render = function () {
        var _a = this.props, style = _a.style, children = _a.children, rtl = _a.rtl;
        /**
         * We are using direction: rtl; to always show the ending of a long overflowing text in input.
         *
         * This however means that the trailing characters with BiDi class O.N. ('Other Neutrals') goes to the other side.
         * Hello! becomes !Hello and vice versa. This is a problem for us when we want to show path in this component, because
         * /user/local/bin becomes user/local/bin/. Wrapping in unicode characters for left-to-righ embedding solves this,
         * however we need to be aware of them when selecting the text - we are solving that by offseting the selectionRange.
         */
        var inputValue = rtl ? '\u202A' + children + '\u202C' : children;
        return (<Wrapper>
        <OverflowContainer>
          <StyledInput readOnly ref={this.textRef} style={style} value={inputValue} onClick={this.handleSelectText} rtl={rtl}/>
        </OverflowContainer>
        <clipboard_1.default hideUnsupported value={children}>
          <StyledCopyButton type="button" size="xsmall" onClick={this.handleCopyClick}>
            <icons_1.IconCopy />
          </StyledCopyButton>
        </clipboard_1.default>
      </Wrapper>);
    };
    return TextCopyInput;
}(React.Component));
exports.default = TextCopyInput;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=textCopyInput.jsx.map