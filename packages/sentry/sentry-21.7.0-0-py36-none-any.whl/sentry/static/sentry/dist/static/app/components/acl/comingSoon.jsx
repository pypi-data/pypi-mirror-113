Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var ComingSoon = function () { return (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
    {locale_1.t('This feature is coming soon!')}
  </alert_1.default>); };
exports.default = ComingSoon;
//# sourceMappingURL=comingSoon.jsx.map