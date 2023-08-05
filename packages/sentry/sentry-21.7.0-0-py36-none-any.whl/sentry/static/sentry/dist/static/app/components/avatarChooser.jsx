Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var avatarCropper_1 = tslib_1.__importDefault(require("app/components/avatarCropper"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var well_1 = tslib_1.__importDefault(require("app/components/well"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var radioGroup_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/radioGroup"));
var AvatarChooser = /** @class */ (function (_super) {
    tslib_1.__extends(AvatarChooser, _super);
    function AvatarChooser() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            model: _this.props.model,
            savedDataUrl: null,
            dataUrl: null,
            hasError: false,
        };
        _this.handleSaveSettings = function (ev) {
            var _a = _this.props, endpoint = _a.endpoint, api = _a.api;
            var _b = _this.state, model = _b.model, dataUrl = _b.dataUrl;
            ev.preventDefault();
            var data = {};
            var avatarType = model && model.avatar ? model.avatar.avatarType : undefined;
            var avatarPhoto = dataUrl ? dataUrl.split(',')[1] : undefined;
            data = {
                avatar_photo: avatarPhoto,
                avatar_type: avatarType,
            };
            api.request(endpoint, {
                method: 'PUT',
                data: data,
                success: function (resp) {
                    _this.setState({ savedDataUrl: _this.state.dataUrl });
                    _this.handleSuccess(resp);
                },
                error: _this.handleError.bind(_this, 'There was an error saving your preferences.'),
            });
        };
        _this.handleChange = function (id) {
            var _a, _b;
            return _this.updateState(tslib_1.__assign(tslib_1.__assign({}, _this.state.model), { avatar: { avatarUuid: (_b = (_a = _this.state.model.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid) !== null && _b !== void 0 ? _b : '', avatarType: id } }));
        };
        return _this;
    }
    AvatarChooser.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // Update local state if defined in props
        if (typeof nextProps.model !== 'undefined') {
            this.setState({ model: nextProps.model });
        }
    };
    AvatarChooser.prototype.updateState = function (model) {
        this.setState({ model: model });
    };
    AvatarChooser.prototype.handleError = function (msg) {
        indicator_1.addErrorMessage(msg);
    };
    AvatarChooser.prototype.handleSuccess = function (model) {
        var onSave = this.props.onSave;
        this.setState({ model: model });
        onSave(model);
        indicator_1.addSuccessMessage(locale_1.t('Successfully saved avatar preferences'));
    };
    AvatarChooser.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, allowGravatar = _c.allowGravatar, allowUpload = _c.allowUpload, allowLetter = _c.allowLetter, savedDataUrl = _c.savedDataUrl, type = _c.type, isUser = _c.isUser, disabled = _c.disabled;
        var _d = this.state, hasError = _d.hasError, model = _d.model;
        if (hasError) {
            return <loadingError_1.default />;
        }
        if (!model) {
            return <loadingIndicator_1.default />;
        }
        var avatarType = (_b = (_a = model.avatar) === null || _a === void 0 ? void 0 : _a.avatarType) !== null && _b !== void 0 ? _b : 'letter_avatar';
        var isLetter = avatarType === 'letter_avatar';
        var isTeam = type === 'team';
        var isOrganization = type === 'organization';
        var choices = [];
        if (allowLetter) {
            choices.push(['letter_avatar', locale_1.t('Use initials')]);
        }
        if (allowUpload) {
            choices.push(['upload', locale_1.t('Upload an image')]);
        }
        if (allowGravatar) {
            choices.push(['gravatar', locale_1.t('Use Gravatar')]);
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Avatar')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <AvatarForm>
            <AvatarGroup inline={isLetter}>
              <radioGroup_1.default style={{ flex: 1 }} choices={choices} value={avatarType} label={locale_1.t('Avatar Type')} onChange={this.handleChange} disabled={disabled}/>
              {isLetter && (<avatar_1.default gravatar={false} style={{ width: 90, height: 90 }} user={isUser ? model : undefined} organization={isOrganization ? model : undefined} team={isTeam ? model : undefined}/>)}
            </AvatarGroup>

            <AvatarUploadSection>
              {allowGravatar && avatarType === 'gravatar' && (<well_1.default>
                  {locale_1.t('Gravatars are managed through ')}
                  <externalLink_1.default href="http://gravatar.com">Gravatar.com</externalLink_1.default>
                </well_1.default>)}

              {model.avatar && avatarType === 'upload' && (<avatarCropper_1.default {...this.props} type={type} model={model} savedDataUrl={savedDataUrl} updateDataUrlState={function (dataState) { return _this.setState(dataState); }}/>)}
              <AvatarSubmit className="form-actions">
                <button_1.default type="button" priority="primary" onClick={this.handleSaveSettings} disabled={disabled}>
                  {locale_1.t('Save Avatar')}
                </button_1.default>
              </AvatarSubmit>
            </AvatarUploadSection>
          </AvatarForm>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    AvatarChooser.defaultProps = {
        allowGravatar: true,
        allowLetter: true,
        allowUpload: true,
        type: 'user',
        onSave: function () { },
    };
    return AvatarChooser;
}(React.Component));
var AvatarGroup = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: ", ";\n"], ["\n  display: flex;\n  flex-direction: ", ";\n"])), function (p) { return (p.inline ? 'row' : 'column'); });
var AvatarForm = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  line-height: 1.5em;\n  padding: 1em 1.25em;\n"], ["\n  line-height: 1.5em;\n  padding: 1em 1.25em;\n"])));
var AvatarSubmit = styled_1.default('fieldset')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 1em;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-top: 1em;\n"])));
var AvatarUploadSection = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: 1em;\n"], ["\n  margin-top: 1em;\n"])));
exports.default = withApi_1.default(AvatarChooser);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=avatarChooser.jsx.map