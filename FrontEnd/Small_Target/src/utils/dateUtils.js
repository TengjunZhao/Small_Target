/**
 * 统一格式化日期为 YYYY-MM-DD 格式（适配数据库存储）
 * @param {Date|String|null} date - 日期对象/日期字符串/空值
 * @returns {String|null} 格式化后的日期字符串（无效值返回null）
 */
export const formatDateForDatabase = (date) => {
  if (!date) return null;

  const d = new Date(date);
  if (isNaN(d.getTime())) {
    console.warn('传入的日期格式无效:', date);
    return null;
  }

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 还可以扩展其他日期工具函数（比如解析数据库日期、加时分秒等）
export const parseDatabaseDate = (dateStr) => {
  if (!dateStr) return null;
  return new Date(dateStr);
};
