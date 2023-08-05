Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var search_1 = tslib_1.__importDefault(require("app/components/search"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var CommandPalette = /** @class */ (function (_super) {
    tslib_1.__extends(CommandPalette, _super);
    function CommandPalette() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CommandPalette.prototype.componentDidMount = function () {
        analytics_1.analytics('omnisearch.open', {});
    };
    CommandPalette.prototype.render = function () {
        var _a = this.props, theme = _a.theme, Body = _a.Body;
        return (<Body>
        <react_2.ClassNames>
          {function (_a) {
                var injectedCss = _a.css;
                return (<search_1.default entryPoint="command_palette" minSearch={1} maxResults={10} dropdownStyle={injectedCss(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "], ["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "])), theme.border)} renderInput={function (_a) {
                        var getInputProps = _a.getInputProps;
                        return (<InputWrapper>
                  <StyledInput autoFocus {...getInputProps({
                            type: 'text',
                            placeholder: locale_1.t('Search for projects, teams, settings, etc...'),
                        })}/>
                </InputWrapper>);
                    }}/>);
            }}
        </react_2.ClassNames>
      </Body>);
    };
    return CommandPalette;
}(react_1.Component));
exports.default = react_2.withTheme(CommandPalette);
exports.modalCss = react_2.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  [role='document'] {\n    padding: 0;\n  }\n"], ["\n  [role='document'] {\n    padding: 0;\n  }\n"])));
var InputWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(0.25));
var StyledInput = styled_1.default(input_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  padding: ", ";\n  border-radius: 8px;\n\n  outline: none;\n  border: none;\n  box-shadow: none;\n\n  :focus,\n  :active,\n  :hover {\n    outline: none;\n    border: none;\n    box-shadow: none;\n  }\n"], ["\n  width: 100%;\n  padding: ", ";\n  border-radius: 8px;\n\n  outline: none;\n  border: none;\n  box-shadow: none;\n\n  :focus,\n  :active,\n  :hover {\n    outline: none;\n    border: none;\n    box-shadow: none;\n  }\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=commandPalette.jsx.map