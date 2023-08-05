Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_select_1 = require("react-select");
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var locale_1 = require("app/locale");
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var defaultProps = {
    avatarSize: 20,
    placeholder: locale_1.t('Choose Sentry project'),
};
var RenderField = /** @class */ (function (_super) {
    tslib_1.__extends(RenderField, _super);
    function RenderField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // need to map the option object to the value
        _this.handleChange = function (onBlur, onChange, optionObj, event) {
            var value = optionObj.value;
            onChange === null || onChange === void 0 ? void 0 : onChange(value, event);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, event);
        };
        return _this;
    }
    RenderField.prototype.render = function () {
        var _a = this.props, projects = _a.projects, avatarSize = _a.avatarSize, onChange = _a.onChange, onBlur = _a.onBlur, rest = tslib_1.__rest(_a, ["projects", "avatarSize", "onChange", "onBlur"]);
        var projectOptions = projects.map(function (_a) {
            var slug = _a.slug, id = _a.id;
            return ({ value: id, label: slug });
        });
        var customOptionProject = function (projectProps) {
            var project = projects.find(function (proj) { return proj.id === projectProps.value; });
            // shouldn't happen but need to account for it
            if (!project) {
                return <react_select_1.components.Option {...projectProps}/>;
            }
            return (<react_select_1.components.Option {...projectProps}>
          <idBadge_1.default project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </react_select_1.components.Option>);
        };
        var customValueContainer = function (containerProps) {
            var selectedValue = containerProps.getValue()[0];
            var project = projects.find(function (proj) { return proj.id === (selectedValue === null || selectedValue === void 0 ? void 0 : selectedValue.value); });
            // shouldn't happen but need to account for it
            if (!project) {
                return <react_select_1.components.ValueContainer {...containerProps}/>;
            }
            return (<react_select_1.components.ValueContainer {...containerProps}>
          <idBadge_1.default project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </react_select_1.components.ValueContainer>);
        };
        return (<selectControl_1.default options={projectOptions} components={{
                Option: customOptionProject,
                ValueContainer: customValueContainer,
            }} {...rest} onChange={this.handleChange.bind(this, onBlur, onChange)}/>);
    };
    RenderField.defaultProps = defaultProps;
    return RenderField;
}(React.Component));
var SentryProjectSelectorField = function (props) { return (<inputField_1.default {...props} field={function (renderProps) { return <RenderField {...renderProps}/>; }}/>); };
exports.default = SentryProjectSelectorField;
//# sourceMappingURL=sentryProjectSelectorField.jsx.map