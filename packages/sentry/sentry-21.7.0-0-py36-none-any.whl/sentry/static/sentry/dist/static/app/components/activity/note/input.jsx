Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_mentions_1 = require("react-mentions");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var text_1 = tslib_1.__importDefault(require("app/styles/text"));
var marked_1 = tslib_1.__importDefault(require("app/utils/marked"));
var mentionables_1 = tslib_1.__importDefault(require("./mentionables"));
var mentionStyle_1 = tslib_1.__importDefault(require("./mentionStyle"));
var defaultProps = {
    placeholder: locale_1.t('Add a comment.\nTag users with @, or teams with #'),
    minHeight: 140,
    busy: false,
};
var NoteInputComponent = /** @class */ (function (_super) {
    tslib_1.__extends(NoteInputComponent, _super);
    function NoteInputComponent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            preview: false,
            value: _this.props.text || '',
            memberMentions: [],
            teamMentions: [],
        };
        _this.handleToggleEdit = function () {
            _this.setState({ preview: false });
        };
        _this.handleTogglePreview = function () {
            _this.setState({ preview: true });
        };
        _this.handleSubmit = function (e) {
            e.preventDefault();
            _this.submitForm();
        };
        _this.handleChange = function (e) {
            _this.setState({ value: e.target.value });
            if (_this.props.onChange) {
                _this.props.onChange(e, { updating: !!_this.props.modelId });
            }
        };
        _this.handleKeyDown = function (e) {
            // Auto submit the form on [meta] + Enter
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                _this.submitForm();
            }
        };
        _this.handleCancel = function (e) {
            e.preventDefault();
            _this.finish();
        };
        _this.handleAddMember = function (id, display) {
            _this.setState(function (_a) {
                var memberMentions = _a.memberMentions;
                return ({
                    memberMentions: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(memberMentions)), [["" + id, display]]),
                });
            });
        };
        _this.handleAddTeam = function (id, display) {
            _this.setState(function (_a) {
                var teamMentions = _a.teamMentions;
                return ({
                    teamMentions: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(teamMentions)), [["" + id, display]]),
                });
            });
        };
        return _this;
    }
    NoteInputComponent.prototype.cleanMarkdown = function (text) {
        return text
            .replace(/\[sentry\.strip:member\]/g, '@')
            .replace(/\[sentry\.strip:team\]/g, '');
    };
    NoteInputComponent.prototype.submitForm = function () {
        if (!!this.props.modelId) {
            this.update();
            return;
        }
        this.create();
    };
    NoteInputComponent.prototype.create = function () {
        var onCreate = this.props.onCreate;
        if (onCreate) {
            onCreate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    };
    NoteInputComponent.prototype.update = function () {
        var onUpdate = this.props.onUpdate;
        if (onUpdate) {
            onUpdate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    };
    NoteInputComponent.prototype.finish = function () {
        this.props.onEditFinish && this.props.onEditFinish();
    };
    NoteInputComponent.prototype.finalizeMentions = function () {
        var _this = this;
        var _a = this.state, memberMentions = _a.memberMentions, teamMentions = _a.teamMentions;
        // each mention looks like [id, display]
        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(memberMentions)), tslib_1.__read(teamMentions)).filter(function (mention) { return _this.state.value.indexOf(mention[1]) !== -1; })
            .map(function (mention) { return mention[0]; });
    };
    NoteInputComponent.prototype.render = function () {
        var _a = this.state, preview = _a.preview, value = _a.value;
        var _b = this.props, modelId = _b.modelId, busy = _b.busy, placeholder = _b.placeholder, minHeight = _b.minHeight, errorJSON = _b.errorJSON, memberList = _b.memberList, teams = _b.teams, theme = _b.theme;
        var existingItem = !!modelId;
        var btnText = existingItem ? locale_1.t('Save Comment') : locale_1.t('Post Comment');
        var errorMessage = (errorJSON &&
            (typeof errorJSON.detail === 'string'
                ? errorJSON.detail
                : (errorJSON.detail && errorJSON.detail.message) ||
                    locale_1.t('Unable to post comment'))) ||
            null;
        return (<NoteInputForm data-test-id="note-input-form" noValidate onSubmit={this.handleSubmit}>
        <NoteInputNavTabs>
          <NoteInputNavTab className={!preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleToggleEdit}>
              {existingItem ? locale_1.t('Edit') : locale_1.t('Write')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <NoteInputNavTab className={preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleTogglePreview}>
              {locale_1.t('Preview')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <MarkdownTab>
            <icons_1.IconMarkdown />
            <MarkdownSupported>{locale_1.t('Markdown supported')}</MarkdownSupported>
          </MarkdownTab>
        </NoteInputNavTabs>

        <NoteInputBody>
          {preview ? (<NotePreview minHeight={minHeight} dangerouslySetInnerHTML={{ __html: marked_1.default(this.cleanMarkdown(value)) }}/>) : (<react_mentions_1.MentionsInput style={mentionStyle_1.default({ theme: theme, minHeight: minHeight })} placeholder={placeholder} onChange={this.handleChange} onKeyDown={this.handleKeyDown} value={value} required autoFocus>
              <react_mentions_1.Mention trigger="@" data={memberList} onAdd={this.handleAddMember} displayTransform={function (_id, display) { return "@" + display; }} markup="**[sentry.strip:member]__display__**" appendSpaceOnAdd/>
              <react_mentions_1.Mention trigger="#" data={teams} onAdd={this.handleAddTeam} markup="**[sentry.strip:team]__display__**" appendSpaceOnAdd/>
            </react_mentions_1.MentionsInput>)}
        </NoteInputBody>

        <Footer>
          <div>{errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}</div>
          <div>
            {existingItem && (<FooterButton priority="danger" type="button" onClick={this.handleCancel}>
                {locale_1.t('Cancel')}
              </FooterButton>)}
            <FooterButton error={errorMessage} type="submit" disabled={busy}>
              {btnText}
            </FooterButton>
          </div>
        </Footer>
      </NoteInputForm>);
    };
    return NoteInputComponent;
}(React.Component));
var NoteInput = react_1.withTheme(NoteInputComponent);
var NoteInputContainer = /** @class */ (function (_super) {
    tslib_1.__extends(NoteInputContainer, _super);
    function NoteInputContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderInput = function (_a) {
            var members = _a.members, teams = _a.teams;
            var _b = _this.props, _ = _b.projectSlugs, props = tslib_1.__rest(_b, ["projectSlugs"]);
            return <NoteInput memberList={members} teams={teams} {...props}/>;
        };
        return _this;
    }
    NoteInputContainer.prototype.render = function () {
        var projectSlugs = this.props.projectSlugs;
        var me = configStore_1.default.get('user');
        return (<mentionables_1.default me={me} projectSlugs={projectSlugs}>
        {this.renderInput}
      </mentionables_1.default>);
    };
    NoteInputContainer.defaultProps = defaultProps;
    return NoteInputContainer;
}(React.Component));
exports.default = NoteInputContainer;
// This styles both the note preview and the note editor input
var getNotePreviewCss = function (p) {
    var _a = mentionStyle_1.default(p)['&multiLine'].input, minHeight = _a.minHeight, padding = _a.padding, overflow = _a.overflow, border = _a.border;
    return "\n  max-height: 1000px;\n  max-width: 100%;\n  " + ((minHeight && "min-height: " + minHeight + "px") || '') + ";\n  padding: " + padding + ";\n  overflow: " + overflow + ";\n  border: " + border + ";\n";
};
var getNoteInputErrorStyles = function (p) {
    if (!p.error) {
        return '';
    }
    return "\n  color: " + p.theme.error + ";\n  margin: -1px;\n  border: 1px solid " + p.theme.error + ";\n  border-radius: " + p.theme.borderRadius + ";\n\n    &:before {\n      display: block;\n      content: '';\n      width: 0;\n      height: 0;\n      border-top: 7px solid transparent;\n      border-bottom: 7px solid transparent;\n      border-right: 7px solid " + p.theme.red300 + ";\n      position: absolute;\n      left: -7px;\n      top: 12px;\n    }\n\n    &:after {\n      display: block;\n      content: '';\n      width: 0;\n      height: 0;\n      border-top: 6px solid transparent;\n      border-bottom: 6px solid transparent;\n      border-right: 6px solid #fff;\n      position: absolute;\n      left: -5px;\n      top: 12px;\n    }\n  ";
};
var NoteInputForm = styled_1.default('form')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 15px;\n  line-height: 22px;\n  transition: padding 0.2s ease-in-out;\n\n  ", "\n"], ["\n  font-size: 15px;\n  line-height: 22px;\n  transition: padding 0.2s ease-in-out;\n\n  ", "\n"])), function (p) { return getNoteInputErrorStyles(p); });
var NoteInputBody = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), text_1.default);
var Footer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  border-top: 1px solid ", ";\n  justify-content: space-between;\n  transition: opacity 0.2s ease-in-out;\n  padding-left: ", ";\n"], ["\n  display: flex;\n  border-top: 1px solid ", ";\n  justify-content: space-between;\n  transition: opacity 0.2s ease-in-out;\n  padding-left: ", ";\n"])), function (p) { return p.theme.border; }, space_1.default(1.5));
var FooterButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  margin: -1px -1px -1px;\n  border-radius: 0 0 ", ";\n\n  ", "\n"], ["\n  font-size: 13px;\n  margin: -1px -1px -1px;\n  border-radius: 0 0 ", ";\n\n  ", "\n"])), function (p) { return p.theme.borderRadius; }, function (p) {
    return p.error &&
        "\n  &, &:active, &:focus, &:hover {\n  border-bottom-color: " + p.theme.error + ";\n  border-right-color: " + p.theme.error + ";\n  }\n  ";
});
var ErrorMessage = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  color: ", ";\n  font-size: 0.9em;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  color: ", ";\n  font-size: 0.9em;\n"])), function (p) { return p.theme.error; });
var NoteInputNavTabs = styled_1.default(navTabs_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  margin-bottom: 0;\n"], ["\n  padding: ", " ", " 0;\n  border-bottom: 1px solid ", ";\n  margin-bottom: 0;\n"])), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; });
var NoteInputNavTab = styled_1.default('li')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-right: 13px;\n"], ["\n  margin-right: 13px;\n"])));
var NoteInputNavTabLink = styled_1.default('a')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  .nav-tabs > li > & {\n    font-size: 15px;\n    padding-bottom: 5px;\n  }\n"], ["\n  .nav-tabs > li > & {\n    font-size: 15px;\n    padding-bottom: 5px;\n  }\n"])));
var MarkdownTab = styled_1.default(NoteInputNavTab)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  .nav-tabs > & {\n    display: flex;\n    align-items: center;\n    margin-right: 0;\n    color: ", ";\n\n    float: right;\n  }\n"], ["\n  .nav-tabs > & {\n    display: flex;\n    align-items: center;\n    margin-right: 0;\n    color: ", ";\n\n    float: right;\n  }\n"])), function (p) { return p.theme.subText; });
var MarkdownSupported = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  font-size: 14px;\n"], ["\n  margin-left: ", ";\n  font-size: 14px;\n"])), space_1.default(0.5));
var NotePreview = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  ", ";\n  padding-bottom: ", ";\n"], ["\n  ", ";\n  padding-bottom: ", ";\n"])), function (p) { return getNotePreviewCss(p); }, space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=input.jsx.map