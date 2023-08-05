Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var forms_1 = require("app/views/settings/components/forms");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var alert_1 = tslib_1.__importDefault(require("./alert"));
var RepositoryEditForm = /** @class */ (function (_super) {
    tslib_1.__extends(RepositoryEditForm, _super);
    function RepositoryEditForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RepositoryEditForm.prototype, "initialData", {
        get: function () {
            var repository = this.props.repository;
            return {
                name: repository.name,
                url: repository.url || '',
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RepositoryEditForm.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'name',
                    type: 'string',
                    required: true,
                    label: locale_1.t('Name of your repository.'),
                },
                {
                    name: 'url',
                    type: 'string',
                    required: false,
                    label: locale_1.t('Full URL to your repository.'),
                    placeholder: locale_1.t('https://github.com/my-org/my-repo/'),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    RepositoryEditForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, onCancel = _a.onCancel, orgSlug = _a.orgSlug, repository = _a.repository;
        var endpoint = "/organizations/" + orgSlug + "/repos/" + repository.id + "/";
        return (<form_1.default initialData={this.initialData} onSubmitSuccess={function (data) {
                _this.props.onSubmitSuccess(data);
                _this.props.closeModal();
            }} apiEndpoint={endpoint} apiMethod="PUT" onCancel={onCancel}>
        <alert_1.default type="warning" icon={<icons_1.IconWarning />}>
          {locale_1.tct('Changing the [name:repo name] may have consequences if it no longer matches the repo name used when [link:sending commits with releases].', {
                link: (<a href="https://docs.sentry.io/product/cli/releases/#sentry-cli-commit-integration"/>),
                name: <strong>repo name</strong>,
            })}
        </alert_1.default>
        {this.formFields.map(function (field) { return (<forms_1.FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>); })}
      </form_1.default>);
    };
    return RepositoryEditForm;
}(react_1.default.Component));
exports.default = RepositoryEditForm;
//# sourceMappingURL=repositoryEditForm.jsx.map