Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var PreviewFeature = function (_a) {
    var _b = _a.type, type = _b === void 0 ? 'info' : _b;
    return (<alert_1.default type={type} icon={<icons_1.IconLab size="sm"/>}>
    {locale_1.t('This feature is a preview and may change in the future. Thanks for being an early adopter!')}
  </alert_1.default>);
};
exports.default = PreviewFeature;
//# sourceMappingURL=previewFeature.jsx.map