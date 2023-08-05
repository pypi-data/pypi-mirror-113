Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var NavigationButtonGroup = function (_a) {
    var links = _a.links, _b = _a.hasNext, hasNext = _b === void 0 ? false : _b, _c = _a.hasPrevious, hasPrevious = _c === void 0 ? false : _c, className = _a.className, size = _a.size, onOldestClick = _a.onOldestClick, onOlderClick = _a.onOlderClick, onNewerClick = _a.onNewerClick, onNewestClick = _a.onNewestClick;
    return (<buttonBar_1.default className={className} merged>
    <button_1.default size={size} to={links[0]} disabled={!hasPrevious} label={locale_1.t('Oldest')} icon={<icons_1.IconPrevious size="xs"/>} onClick={onOldestClick}/>
    <button_1.default size={size} to={links[1]} disabled={!hasPrevious} onClick={onOlderClick}>
      {locale_1.t('Older')}
    </button_1.default>
    <button_1.default size={size} to={links[2]} disabled={!hasNext} onClick={onNewerClick}>
      {locale_1.t('Newer')}
    </button_1.default>
    <button_1.default size={size} to={links[3]} disabled={!hasNext} label={locale_1.t('Newest')} icon={<icons_1.IconNext size="xs"/>} onClick={onNewestClick}/>
  </buttonBar_1.default>);
};
exports.default = NavigationButtonGroup;
//# sourceMappingURL=navigationButtonGroup.jsx.map