Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
function RoleSelectControl(_a) {
    var roles = _a.roles, disableUnallowed = _a.disableUnallowed, props = tslib_1.__rest(_a, ["roles", "disableUnallowed"]);
    return (<selectControl_1.default options={roles === null || roles === void 0 ? void 0 : roles.map(function (r) {
            return ({
                value: r.id,
                label: r.name,
                disabled: disableUnallowed && !r.allowed,
                description: r.desc,
            });
        })} components={{
            Option: function (_a) {
                var label = _a.label, data = _a.data, optionProps = tslib_1.__rest(_a, ["label", "data"]);
                return (<react_select_1.components.Option label={label} {...optionProps}>
            <RoleItem>
              <h1>{label}</h1>
              <div>{data.description}</div>
            </RoleItem>
          </react_select_1.components.Option>);
            },
        }} styles={{
            control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { borderBottomLeftRadius: theme_1.default.borderRadius, borderBottomRightRadius: theme_1.default.borderRadius })); },
            menu: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { borderRadius: theme_1.default.borderRadius, marginTop: space_1.default(0.5), width: '350px', overflow: 'hidden' })); },
        }} {...props}/>);
}
var RoleItem = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"])), space_1.default(1), function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.25));
exports.default = RoleSelectControl;
var templateObject_1;
//# sourceMappingURL=roleSelectControl.jsx.map