Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var callIfFunction_1 = require("app/utils/callIfFunction");
var slugify_1 = tslib_1.__importDefault(require("app/utils/slugify"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var CreateTeamForm = /** @class */ (function (_super) {
    tslib_1.__extends(CreateTeamForm, _super);
    function CreateTeamForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (data, onSuccess, onError) {
            callIfFunction_1.callIfFunction(_this.props.onSubmit, data, onSuccess, onError);
        };
        _this.handleCreateTeamSuccess = function (data) {
            callIfFunction_1.callIfFunction(_this.props.onSuccess, data);
        };
        return _this;
    }
    CreateTeamForm.prototype.render = function () {
        var organization = this.props.organization;
        return (<react_1.Fragment>
        <p>
          {locale_1.t('Members of a team have access to specific areas, such as a new release or a new application feature.')}
        </p>

        <form_1.default submitLabel={locale_1.t('Create Team')} apiEndpoint={"/organizations/" + organization.slug + "/teams/"} apiMethod="POST" onSubmit={this.handleSubmit} onSubmitSuccess={this.handleCreateTeamSuccess} requireChanges data-test-id="create-team-form" {...this.props.formProps}>
          <textField_1.default name="slug" label={locale_1.t('Team Name')} placeholder={locale_1.t('e.g. operations, web-frontend, desktop')} help={locale_1.t('May contain lowercase letters, numbers, dashes and underscores.')} required stacked flexibleControlStateSize inline={false} transformInput={slugify_1.default}/>
        </form_1.default>
      </react_1.Fragment>);
    };
    return CreateTeamForm;
}(react_1.Component));
exports.default = CreateTeamForm;
//# sourceMappingURL=createTeamForm.jsx.map