Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var scroll_to_element_1 = tslib_1.__importDefault(require("scroll-to-element"));
var utils_1 = require("app/utils");
var sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
var formPanel_1 = tslib_1.__importDefault(require("./formPanel"));
var JsonForm = /** @class */ (function (_super) {
    tslib_1.__extends(JsonForm, _super);
    function JsonForm() {
        var _a;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = {
            // location.hash is optional because of tests.
            highlighted: (_a = _this.props.location) === null || _a === void 0 ? void 0 : _a.hash,
        };
        return _this;
    }
    JsonForm.prototype.componentDidMount = function () {
        this.scrollToHash();
    };
    JsonForm.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.location.hash !== nextProps.location.hash) {
            var hash = nextProps.location.hash;
            this.scrollToHash(hash);
            this.setState({ highlighted: hash });
        }
    };
    JsonForm.prototype.scrollToHash = function (toHash) {
        var _a;
        // location.hash is optional because of tests.
        var hash = toHash || ((_a = this.props.location) === null || _a === void 0 ? void 0 : _a.hash);
        if (!hash) {
            return;
        }
        // Push onto callback queue so it runs after the DOM is updated,
        // this is required when navigating from a different page so that
        // the element is rendered on the page before trying to getElementById.
        try {
            scroll_to_element_1.default(sanitizeQuerySelector_1.sanitizeQuerySelector(decodeURIComponent(hash)), {
                align: 'middle',
                offset: -100,
            });
        }
        catch (err) {
            Sentry.captureException(err);
        }
    };
    JsonForm.prototype.shouldDisplayForm = function (fields) {
        var fieldsWithVisibleProp = fields.filter(function (field) { return typeof field !== 'function' && utils_1.defined(field === null || field === void 0 ? void 0 : field.visible); });
        if (fields.length === fieldsWithVisibleProp.length) {
            var _a = this.props, additionalFieldProps_1 = _a.additionalFieldProps, props_1 = tslib_1.__rest(_a, ["additionalFieldProps"]);
            var areAllFieldsHidden = fieldsWithVisibleProp.every(function (field) {
                if (typeof field.visible === 'function') {
                    return !field.visible(tslib_1.__assign(tslib_1.__assign({}, props_1), additionalFieldProps_1));
                }
                return !field.visible;
            });
            return !areAllFieldsHidden;
        }
        return true;
    };
    JsonForm.prototype.renderForm = function (_a) {
        var fields = _a.fields, formPanelProps = _a.formPanelProps, title = _a.title;
        var shouldDisplayForm = this.shouldDisplayForm(fields);
        if (!shouldDisplayForm &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderFooter) &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderHeader)) {
            return null;
        }
        return <formPanel_1.default title={title} fields={fields} {...formPanelProps}/>;
    };
    JsonForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, access = _a.access, fields = _a.fields, title = _a.title, forms = _a.forms, disabled = _a.disabled, features = _a.features, additionalFieldProps = _a.additionalFieldProps, renderFooter = _a.renderFooter, renderHeader = _a.renderHeader, _location = _a.location, otherProps = tslib_1.__rest(_a, ["access", "fields", "title", "forms", "disabled", "features", "additionalFieldProps", "renderFooter", "renderHeader", "location"]);
        var formPanelProps = {
            access: access,
            disabled: disabled,
            features: features,
            additionalFieldProps: additionalFieldProps,
            renderFooter: renderFooter,
            renderHeader: renderHeader,
            highlighted: this.state.highlighted,
        };
        return (<div {...otherProps}>
        {typeof forms !== 'undefined' &&
                forms.map(function (formGroup, i) { return (<React.Fragment key={i}>
              {_this.renderForm(tslib_1.__assign({ formPanelProps: formPanelProps }, formGroup))}
            </React.Fragment>); })}
        {typeof forms === 'undefined' &&
                typeof fields !== 'undefined' &&
                this.renderForm({ fields: fields, formPanelProps: formPanelProps, title: title })}
      </div>);
    };
    return JsonForm;
}(React.Component));
exports.default = react_router_1.withRouter(JsonForm);
//# sourceMappingURL=jsonForm.jsx.map