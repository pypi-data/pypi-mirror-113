Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var locale_1 = require("app/locale");
var integrationUtil_1 = require("app/utils/integrationUtil");
var forms_1 = require("app/views/settings/components/forms");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var RepositoryProjectPathConfigForm = /** @class */ (function (_super) {
    tslib_1.__extends(RepositoryProjectPathConfigForm, _super);
    function RepositoryProjectPathConfigForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "initialData", {
        get: function () {
            var _a = this.props, existingConfig = _a.existingConfig, integration = _a.integration;
            return tslib_1.__assign({ defaultBranch: 'master', stackRoot: '', sourceRoot: '', repositoryId: existingConfig === null || existingConfig === void 0 ? void 0 : existingConfig.repoId, integrationId: integration.id }, pick_1.default(existingConfig, ['projectId', 'defaultBranch', 'stackRoot', 'sourceRoot']));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RepositoryProjectPathConfigForm.prototype, "formFields", {
        get: function () {
            var _a = this.props, projects = _a.projects, repos = _a.repos;
            var repoChoices = repos.map(function (_a) {
                var name = _a.name, id = _a.id;
                return ({ value: id, label: name });
            });
            return [
                {
                    name: 'projectId',
                    type: 'sentry_project_selector',
                    required: true,
                    label: locale_1.t('Project'),
                    projects: projects,
                },
                {
                    name: 'repositoryId',
                    type: 'select',
                    required: true,
                    label: locale_1.t('Repo'),
                    placeholder: locale_1.t('Choose repo'),
                    options: repoChoices,
                },
                {
                    name: 'defaultBranch',
                    type: 'string',
                    required: true,
                    label: locale_1.t('Branch'),
                    placeholder: locale_1.t('Type your branch'),
                    showHelpInTooltip: true,
                    help: locale_1.t('If an event does not have a release tied to a commit, we will use this branch when linking to your source code.'),
                },
                {
                    name: 'stackRoot',
                    type: 'string',
                    required: false,
                    label: locale_1.t('Stack Trace Root'),
                    placeholder: locale_1.t('Type root path of your stack traces'),
                    showHelpInTooltip: true,
                    help: locale_1.t('Any stack trace starting with this path will be mapped with this rule. An empty string will match all paths.'),
                },
                {
                    name: 'sourceRoot',
                    type: 'string',
                    required: false,
                    label: locale_1.t('Source Code Root'),
                    placeholder: locale_1.t('Type root path of your source code, e.g. `src/`.'),
                    showHelpInTooltip: true,
                    help: locale_1.t('When a rule matches, the stack trace root is replaced with this path to get the path in your repository. Leaving this empty means replacing the stack trace root with an empty string.'),
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    RepositoryProjectPathConfigForm.prototype.handlePreSubmit = function () {
        integrationUtil_1.trackIntegrationEvent('integrations.stacktrace_submit_config', {
            setup_type: 'manual',
            view: 'integration_configuration_detail',
            provider: this.props.integration.provider.key,
        }, this.props.organization);
    };
    RepositoryProjectPathConfigForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, onSubmitSuccess = _a.onSubmitSuccess, onCancel = _a.onCancel, existingConfig = _a.existingConfig;
        // endpoint changes if we are making a new row or updating an existing one
        var baseEndpoint = "/organizations/" + organization.slug + "/code-mappings/";
        var endpoint = existingConfig
            ? "" + baseEndpoint + existingConfig.id + "/"
            : baseEndpoint;
        var apiMethod = existingConfig ? 'PUT' : 'POST';
        return (<form_1.default onSubmitSuccess={onSubmitSuccess} onPreSubmit={function () { return _this.handlePreSubmit(); }} initialData={this.initialData} apiEndpoint={endpoint} apiMethod={apiMethod} onCancel={onCancel}>
        {this.formFields.map(function (field) { return (<forms_1.FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>); })}
      </form_1.default>);
    };
    return RepositoryProjectPathConfigForm;
}(react_1.Component));
exports.default = RepositoryProjectPathConfigForm;
//# sourceMappingURL=repositoryProjectPathConfigForm.jsx.map