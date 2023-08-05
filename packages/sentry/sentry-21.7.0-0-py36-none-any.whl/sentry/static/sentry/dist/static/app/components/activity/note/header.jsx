Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var author_1 = tslib_1.__importDefault(require("app/components/activity/author"));
var linkWithConfirmation_1 = tslib_1.__importDefault(require("app/components/links/linkWithConfirmation"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var editorTools_1 = tslib_1.__importDefault(require("./editorTools"));
var NoteHeader = function (_a) {
    var authorName = _a.authorName, user = _a.user, onEdit = _a.onEdit, onDelete = _a.onDelete;
    var activeUser = configStore_1.default.get('user');
    var canEdit = activeUser && (activeUser.isSuperuser || user.id === activeUser.id);
    return (<div>
      <author_1.default>{authorName}</author_1.default>
      {canEdit && (<editorTools_1.default>
          <tooltip_1.default title={locale_1.t('You can edit this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <Edit onClick={onEdit}>{locale_1.t('Edit')}</Edit>
          </tooltip_1.default>
          <tooltip_1.default title={locale_1.t('You can delete this comment due to your superuser status')} disabled={!activeUser.isSuperuser}>
            <linkWithConfirmation_1.default title={locale_1.t('Remove')} message={locale_1.t('Are you sure you wish to delete this comment?')} onConfirm={onDelete}>
              <Remove>{locale_1.t('Remove')}</Remove>
            </linkWithConfirmation_1.default>
          </tooltip_1.default>
        </editorTools_1.default>)}
    </div>);
};
var getActionStyle = function (p) { return "\n  padding: 0 7px;\n  color: " + p.theme.gray200 + ";\n  font-weight: normal;\n"; };
var Edit = styled_1.default('a')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  margin-left: 7px;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  ", ";\n  margin-left: 7px;\n\n  &:hover {\n    color: ", ";\n  }\n"])), getActionStyle, function (p) { return p.theme.gray300; });
var Remove = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", ";\n  border-left: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  ", ";\n  border-left: 1px solid ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), getActionStyle, function (p) { return p.theme.border; }, function (p) { return p.theme.error; });
exports.default = NoteHeader;
var templateObject_1, templateObject_2;
//# sourceMappingURL=header.jsx.map