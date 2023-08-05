Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var intersection_1 = tslib_1.__importDefault(require("lodash/intersection"));
var indicator_1 = require("app/actionCreators/indicator");
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
/**
 * Given an array of scopes, return the choices the user has picked for each option
 * @param scopes {Array}
 */
var getPermissionSelectionsFromScopes = function (scopes) {
    var e_1, _a;
    var permissions = [];
    try {
        for (var SENTRY_APP_PERMISSIONS_1 = tslib_1.__values(constants_1.SENTRY_APP_PERMISSIONS), SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next(); !SENTRY_APP_PERMISSIONS_1_1.done; SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next()) {
            var permObj = SENTRY_APP_PERMISSIONS_1_1.value;
            var highestChoice = void 0;
            for (var perm in permObj.choices) {
                var choice = permObj.choices[perm];
                var scopesIntersection = intersection_1.default(choice.scopes, scopes);
                if (scopesIntersection.length > 0 &&
                    scopesIntersection.length === choice.scopes.length) {
                    if (!highestChoice || scopesIntersection.length > highestChoice.scopes.length) {
                        highestChoice = choice;
                    }
                }
            }
            if (highestChoice) {
                // we can remove the read part of "Read & Write"
                var label = highestChoice.label.replace('Read & Write', 'Write');
                permissions.push(permObj.resource + " " + label);
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (SENTRY_APP_PERMISSIONS_1_1 && !SENTRY_APP_PERMISSIONS_1_1.done && (_a = SENTRY_APP_PERMISSIONS_1.return)) _a.call(SENTRY_APP_PERMISSIONS_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return permissions;
};
var PublishRequestFormModel = /** @class */ (function (_super) {
    tslib_1.__extends(PublishRequestFormModel, _super);
    function PublishRequestFormModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PublishRequestFormModel.prototype.getTransformedData = function () {
        var data = this.getData();
        // map object to list of questions
        var questionnaire = Array.from(this.fieldDescriptor.values()).map(function (field) {
            // we read the meta for the question that has a react node for the label
            return ({
                question: field.meta || field.label,
                answer: data[field.name],
            });
        });
        return { questionnaire: questionnaire };
    };
    return PublishRequestFormModel;
}(model_1.default));
var SentryAppPublishRequestModal = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppPublishRequestModal, _super);
    function SentryAppPublishRequestModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.form = new PublishRequestFormModel();
        _this.handleSubmitSuccess = function () {
            indicator_1.addSuccessMessage(locale_1.t('Request to publish %s successful.', _this.props.app.slug));
            _this.props.closeModal();
        };
        _this.handleSubmitError = function (err) {
            var _a;
            indicator_1.addErrorMessage(locale_1.tct('Request to publish [app] fails. [detail]', {
                app: _this.props.app.slug,
                detail: (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail,
            }));
        };
        return _this;
    }
    Object.defineProperty(SentryAppPublishRequestModal.prototype, "formFields", {
        get: function () {
            var app = this.props.app;
            var permissions = getPermissionSelectionsFromScopes(app.scopes);
            var permissionQuestionBaseText = 'Please justify why you are requesting each of the following permissions: ';
            var permissionQuestionPlainText = "" + permissionQuestionBaseText + permissions.join(', ') + ".";
            var permissionLabel = (<react_1.Fragment>
        <PermissionLabel>{permissionQuestionBaseText}</PermissionLabel>
        {permissions.map(function (permission, i) { return (<react_1.Fragment key={permission}>
            {i > 0 && ', '} <Permission>{permission}</Permission>
          </react_1.Fragment>); })}
        .
      </react_1.Fragment>);
            // No translations since we need to be able to read this email :)
            var baseFields = [
                {
                    type: 'textarea',
                    required: true,
                    label: 'What does your integration do? Please be as detailed as possible.',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question0',
                },
                {
                    type: 'textarea',
                    required: true,
                    label: 'What value does it offer customers?',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question1',
                },
                {
                    type: 'textarea',
                    required: true,
                    label: 'Do you operate the web service your integration communicates with?',
                    autosize: true,
                    rows: 1,
                    inline: false,
                    name: 'question2',
                },
            ];
            // Only add the permissions question if there are perms to add
            if (permissions.length > 0) {
                baseFields.push({
                    type: 'textarea',
                    required: true,
                    label: permissionLabel,
                    autosize: true,
                    rows: 1,
                    inline: false,
                    meta: permissionQuestionPlainText,
                    name: 'question3',
                });
            }
            return baseFields;
        },
        enumerable: false,
        configurable: true
    });
    SentryAppPublishRequestModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, app = _a.app, Header = _a.Header, Body = _a.Body;
        var endpoint = "/sentry-apps/" + app.slug + "/publish-request/";
        var forms = [
            {
                title: locale_1.t('Questions to answer'),
                fields: this.formFields,
            },
        ];
        return (<react_1.Fragment>
        <Header>{locale_1.t('Publish Request Questionnaire')}</Header>
        <Body>
          <Explanation>
            {locale_1.t("Please fill out this questionnaire in order to get your integration evaluated for publication.\n              Once your integration has been approved, users outside of your organization will be able to install it.")}
          </Explanation>
          <form_1.default allowUndo apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} model={this.form} submitLabel={locale_1.t('Request Publication')} onCancel={function () { return _this.props.closeModal(); }}>
            <jsonForm_1.default forms={forms}/>
          </form_1.default>
        </Body>
      </react_1.Fragment>);
    };
    return SentryAppPublishRequestModal;
}(react_1.Component));
exports.default = SentryAppPublishRequestModal;
var Explanation = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0px;\n  font-size: 18px;\n"], ["\n  margin: ", " 0px;\n  font-size: 18px;\n"])), space_1.default(1.5));
var PermissionLabel = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var Permission = styled_1.default('code')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sentryAppPublishRequestModal.jsx.map