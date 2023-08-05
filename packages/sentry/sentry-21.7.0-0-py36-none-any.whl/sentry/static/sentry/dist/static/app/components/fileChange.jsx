Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
var fileIcon_1 = tslib_1.__importDefault(require("app/components/fileIcon"));
var listGroup_1 = require("app/components/listGroup");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var FileChange = function (_a) {
    var filename = _a.filename, authors = _a.authors, className = _a.className;
    return (<FileItem className={className}>
    <Filename>
      <StyledFileIcon fileName={filename}/>
      <textOverflow_1.default>{filename}</textOverflow_1.default>
    </Filename>
    <div>
      <avatarList_1.default users={authors} avatarSize={25} typeMembers="authors"/>
    </div>
  </FileItem>);
};
var FileItem = styled_1.default(listGroup_1.ListGroupItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var Filename = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  margin-right: ", ";\n  align-items: center;\n  grid-template-columns: max-content 1fr;\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  margin-right: ", ";\n  align-items: center;\n  grid-template-columns: max-content 1fr;\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(3));
var StyledFileIcon = styled_1.default(fileIcon_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  border-radius: 3px;\n"], ["\n  color: ", ";\n  border-radius: 3px;\n"])), function (p) { return p.theme.gray200; });
exports.default = FileChange;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=fileChange.jsx.map