Object.defineProperty(exports, "__esModule", { value: true });
var locale_1 = require("app/locale");
var styles_1 = require("./styles");
var Header = function () { return (<styles_1.Grid>
    <styles_1.GridCell>{locale_1.t('Id')}</styles_1.GridCell>
    <styles_1.GridCell>{locale_1.t('Name')}</styles_1.GridCell>
    <styles_1.GridCell>{locale_1.t('Label')}</styles_1.GridCell>
    <styles_1.GridCell>{locale_1.t('Filename')}</styles_1.GridCell>
    <styles_1.GridCell>{locale_1.t('Status')}</styles_1.GridCell>
  </styles_1.Grid>); };
exports.default = Header;
//# sourceMappingURL=header.jsx.map